'''DBus service utilities for unit tests. 

* Wrappers around openheating's DBus service executables. Reliable
  starting and stopping (checking presence of bus names).
* "Controller" for sequenced startup/shutdown.
'''

from . import testutils

from openheating.error import HeatingError
from openheating.dbus import dbusutil

import pydbus

import tempfile
import subprocess
import sys
import unittest


class ServiceTestCase(unittest.TestCase):
    @staticmethod
    def intercept_failure(testmethod):
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return testmethod(*args, **kwargs)
            except:
                self.__failure = True
        return wrapper

    def setUp(self):
        self.__controller = Controller()
        self.__failure = False
    def tearDown(self):
        self.__controller.stop(print_stderr=self.__failure)
        del self.__controller

    def add_service(self, s):
        self.__controller.add_service(s)
    def start_services(self):
        self.__controller.start()
    def stop_services(self, print_stderr):
        self.__controller.stop(print_stderr=print_stderr)

class Controller:
    '''Start and stop a list of service wrappers.

    '''

    def __init__(self):
        self.__services = []
        self.__running = False

    def start(self):
        self.__running = True
        for s in self.__services:
            s.start()

    def stop(self, print_stderr):
        self.__running = False
        errors = []
        for s in self.__services:
            try:
                s.stop(print_stderr=print_stderr)
            except Exception as e:
                errors.append(e)
        if len(errors) != 0:
            msg = ['there were errors while stopping services ...']
            for e in errors:
                msg.append(str(e))
            raise RuntimeError('\n'.join(msg))

    def add_service(self, s):
        assert not self.__running
        self.__services.append(s)

class _ServiceWrapper:
    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__argv = [testutils.find_executable(exe), '--session', '--log-level', 'debug']
        if args is not None:
            self.__argv += args
        self.__process = None
        self.stderr = None

    def start(self):
        # check if busname is already taken. if so, it makes no sense
        # to start the service; rather, fail right away
        with pydbus.SessionBus() as bus:
            with bus.request_name(self.__busname): pass

        self.__process = subprocess.Popen(self.__argv, stderr=subprocess.PIPE)

        # wait until busname appears
        completed_process = subprocess.run(
            ['gdbus', 'wait', '--session', self.__busname, '--timeout', '5'],
        )
        if completed_process.returncode != 0:
            # busname did not appear within the given
            # timeout. terminate service process, output its stderr if
            # any.
            self.__process.terminate()
            self.__process.wait()
            self.stderr = str(self.__process.stderr.read(), encoding='ascii')
            rc = self.__process.returncode
            self.__process = None

            raise HeatingError('start: name {} did not appear within timeout, '
                               'stderr:\n{}'.format(self.__busname, self.indented_stderr()))

    def stop(self, print_stderr):
        if self.__process is None:
            return

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

        self.stderr = str(self.__process.stderr.read(), encoding='ascii')

        if print_stderr or self.__process.returncode != 0:
            raise HeatingError('stop: service {} exited with status {}, '
                               'stderr:\n{}'.format(self.__busname, self.__process.returncode, self.indented_stderr()))

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

    def indented_stderr(self):
        lines = self.stderr.split('\n')
        lines = ['  {}: {}'.format(self.__busname, line) for line in lines]
        return '\n'.join(lines)

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
                         busname=dbusutil.THERMOMETERS_BUSNAME,
                         args=confargs)

    def stop(self, print_stderr):
        super().stop(print_stderr=print_stderr)
        self.__configfile.close()

class ErrorService(_ServiceWrapper):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-errors.py',
            busname=dbusutil.ERRORS_BUSNAME)

class ExceptionTesterService(_ServiceWrapper):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=dbusutil.EXCEPTIONTESTER_BUSNAME,
        )

class ManagedObjectTesterService(_ServiceWrapper):
    def __init__(self, stampdir, debug=False):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=dbusutil.MANAGEDOBJECTTESTER_BUSNAME,
            args=['--stamp-directory', stampdir],
        )
