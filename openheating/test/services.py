'''DBus service utilities for unit tests. 

* Wrappers around openheating's DBus service executables. Reliable
  starting and stopping (checking presence of bus names).
'''

from . import testutils

from openheating.error import HeatingError
from openheating.dbus import names

import pydbus

import tempfile
import subprocess
import sys
import unittest


class ServiceTestCase(unittest.TestCase):
    '''TestCase derivative which is good at managing dbus services as
    subprocesses.

    If failure is detected (see the decorator), then at tearDown the
    stderr output of each service is printed.

    '''

    @staticmethod
    def intercept_failure(testmethod):
        '''test method decorator to intercept test case failures (these are
        hard to come by otherwise)'''
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return testmethod(*args, **kwargs)
            except:
                self.__failure = True
                raise
        return wrapper

    def setUp(self):
        self.__failure = False
        self.__services = None
    def tearDown(self):
        self.stop_services()

    def start_services(self, services):
        assert self.__services is None
        self.__services = services
        for s in self.__services:
            s.start()

    def stop_services(self, print_stderr=False):
        if self.__services is None:
            services = []
        else:
            services = self.__services
        self.__services = None

        stderrs = []
        errors = []
        for s in services:
            try:
                stderr = s.stop(print_stderr=self.__failure or print_stderr)
                stderrs.append((s.busname, stderr))
            except Exception as e:
                errors.append(e)

        if print_stderr or self.__failure or len(errors):
            for busname, stderr in stderrs:
                print('\n*** STDERR from {}'.format(busname), file=sys.stderr)
                if stderr is None:
                    print(' '*3, '(apparently unstarted)', file=sys.stderr)
                else:
                    for line in stderr.split('\n'):
                        print(' '*3, line, file=sys.stderr)

        if len(errors):
            msg = ['there were errors while stopping services ...']
            for e in errors:
                msg.append(str(e))
            raise RuntimeError('\n'.join(msg))

class _ServiceWrapper:
    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__argv = [testutils.find_executable(exe), '--session', '--log-level', 'debug']
        if args is not None:
            self.__argv += args
        self.__process = None

    @property
    def busname(self):
        return self.__busname

    def start(self):
        # check if busname is already taken. if so, it makes no sense
        # to start the service; rather, fail right away
        with pydbus.SessionBus() as bus:
            with bus.request_name(self.__busname): pass

        self.__process = subprocess.Popen(self.__argv, stderr=subprocess.PIPE)

        # wait until busname appears
        gdbus_wait = ['gdbus', 'wait', '--session', self.__busname, '--timeout', '5']
        completed_process = subprocess.run(gdbus_wait)

        if completed_process.returncode != 0:
            # busname did not appear within the given
            # timeout. terminate service process, output its stderr if
            # any.
            self.__process.terminate()
            self.__process.wait()
            stderr = str(self.__process.stderr.read(), encoding='ascii')
            rc = self.__process.returncode
            self.__process = None

            raise HeatingError('start: name {busname} did not appear within timeout, '
                               'stderr from "{gdbus}":\n{stderr}'.format(
                                   busname=self.__busname, 
                                   gdbus=' '.join(gdbus_wait),
                                   stderr=stderr))

    def stop(self, print_stderr):
        if self.__process is None:
            return None

        self.__process.terminate()
        # our services mess with signals a bit (graceful eventloop
        # termination), so apply a timeout in case anything goes
        # wrong.
        try:
            self.__process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(' '.join(self.__argv), 'refuses to terminate, killing', file=sys.stderr)
            self.__process.kill()
            self.__process.wait()

        stderr = str(self.__process.stderr.read(), encoding='ascii')
        exc = None

        if self.__process.returncode != 0:
            exc = HeatingError('stop: name {busname} exited with status {status}, '
                               'stderr:\n{stderr}'.format(
                                   busname=self.__busname, 
                                   status=self.__process.returncode, 
                                   stderr=stderr))

        # wait for busname to disappear
        for _ in range(10):
            completed_process = subprocess.run(
                ['gdbus', 'call', '--session', '--dest', 'org.freedesktop.DBus',
                 '--object-path', '/org/freedesktop/DBus', '--method', 'org.freedesktop.DBus.ListNames'],
                stdout=subprocess.PIPE,
                check=True,
            )
            names = eval(completed_process.stdout)
            
            if self.__busname in names:
                time.sleep(0.5)
                continue
            else:
                break
        else:
            self.fail('{} still on the bus'.format(self.__busname))

        if exc is not None:
            raise exc
        return stderr

class ThermometerService(_ServiceWrapper):
    def __init__(self, conf=None, pyconf=None, debug=False):
        self.__configfile = tempfile.NamedTemporaryFile(mode='w')
        if conf is not None:
            confargs = ['--configfile', self.__configfile.name]
        else:
            assert pyconf is not None
            confargs = ['--pyconfigfile', self.__configfile.name]

        self.__configfile.write('\n'.join(conf or pyconf))
        self.__configfile.flush()

        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         args=confargs)

    def stop(self, print_stderr):
        super().stop(print_stderr=print_stderr)
        self.__configfile.close()

class ErrorService(_ServiceWrapper):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-errors.py',
            busname=names.Bus.ERRORS)

class ExceptionTesterService(_ServiceWrapper):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=names.Bus.EXCEPTIONTESTER,
        )

class ManagedObjectTesterService(_ServiceWrapper):
    def __init__(self, stampdir, debug=False):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=names.Bus.MANAGEDOBJECTTESTER,
            args=['--stamp-directory', stampdir],
        )
