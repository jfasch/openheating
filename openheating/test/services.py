'''DBus service utilities for unit tests. 

* Wrappers around openheating's DBus service executables. Reliable
  starting and stopping (checking presence of bus names).
'''

from . import testutils

from ..base.error import HeatingError
from ..dbus import names

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

        started = []
        start_error = None
        for s in self.__services:
            try:
                s.start()
                started.append(s)
            except HeatingError as e:
                start_error = e

        if start_error is not None:
            for s in reversed(started):
                s.stop()
            raise start_error

    def stop_services(self):
        if self.__services is None:
            services = []
        else:
            services = self.__services
        self.__services = None

        stderrs = []
        errors = []
        for s in services:
            try:
                stderr = s.stop()
                stderrs.append((s.busname, stderr))
            except Exception as e:
                errors.append(e)

        if self.__failure or len(errors):
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
        service_cmdline = ' '.join(self.__argv)

        # check if busname is already taken. if so, it makes no sense
        # to start the service; rather, fail right away
        with pydbus.SessionBus() as bus:
            name_occupied = False
            try:
                with bus.request_name(self.__busname): pass
            except RuntimeError:
                name_occupied = True
            if name_occupied:
                raise HeatingError('start: {busname} already occupied, no point in starting "{cmdline}"'.format(
                    busname=self.__busname, cmdline=service_cmdline))

        # start service, and wait until its busname appears.
        self.__process = subprocess.Popen(self.__argv, stderr=subprocess.PIPE, universal_newlines=True)
        for _ in range(5):
            gdbus_wait = ['gdbus', 'wait', '--session', self.__busname, '--timeout', '1']
            completed_process = subprocess.run(gdbus_wait)
            if completed_process.returncode == 0:
                break

            # busname not yet taken. see if process has exited.
            try:
                self.__process.wait(timeout=0)
                _, stderr = self.__process.communicate()

                raise HeatingError('start: {busname} not taken within timeout, "{cmdline}" has exited with status {status}, stderr:\n{stderr}'.format(
                    busname=self.__busname,
                    cmdline=service_cmdline,
                    status=self.__process.returncode,
                    stderr=_indent_str(stderr)))
            except subprocess.TimeoutExpired:
                continue
        else:
            # busname did not appear within the given timeout (5 times
            # 1 second). terminate service process.
            self.__process.terminate()
            self.__process.wait()
            _, stderr = self.__process.communicate()
            raise HeatingError('start: name {busname} did not appear within timeout: "{cmdline}", stderr:\n{stderr}'.format(
                busname=self.__busname, 
                cmdline=service_cmdline,
                stderr=_indent_str(stderr)))

    def stop(self):
        assert self.__process.returncode is None, "stop() must not be called if start() hasn't succeeded"

        # terminate service process
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

        _, stderr = self.__process.communicate()

        # wait for busname to disappear
        with pydbus.SessionBus() as bus:
            proxy = bus.get('org.freedesktop.DBus', '/org/freedesktop/DBus')['org.freedesktop.DBus']
            for _ in range(10):
                if self.__busname in proxy.ListNames():
                    time.sleep(0.5)
                    continue
                else:
                    break
            else:
                # hmm. process has terminated? name still taken?
                self.fail('{busname} still on the bus after "{cmdline}" has exited (?)'.format(
                    busname=self.__busname, cmdline=' '.join(self.__argv)))

        if self.__process.returncode != 0:
            raise HeatingError('stop: name {busname} exited with status {status}, '
                               'stderr:\n{stderr}'.format(
                                   busname=self.__busname, 
                                   status=self.__process.returncode, 
                                   stderr=_indent_str(stderr)))

        return stderr

def _indent_str(s):
    return s.replace('\n', '\n    ')

class ThermometerService(_ServiceWrapper):
    def __init__(self, pyconf, debug=False):
        self.__pyconfigfile = tempfile.NamedTemporaryFile(mode='w')
        confargs = ['--pyconfigfile', self.__pyconfigfile.name]

        self.__pyconfigfile.write('\n'.join(pyconf))
        self.__pyconfigfile.flush()

        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         args=confargs)

    def stop(self):
        self.__pyconfigfile.close()
        return super().stop()

class SwitchService(_ServiceWrapper):
    def __init__(self, pyconf, debug=False):
        self.__pyconfigfile = tempfile.NamedTemporaryFile(mode='w')
        confargs = ['--pyconfigfile', self.__pyconfigfile.name]

        self.__pyconfigfile.write('\n'.join(pyconf))
        self.__pyconfigfile.flush()

        super().__init__(exe='openheating-switches.py',
                         busname=names.Bus.SWITCHES,
                         args=confargs)

    def stop(self):
        self.__pyconfigfile.close()
        return super().stop()

class CircuitService(_ServiceWrapper):
    def __init__(self, pyconf, debug=False):
        self.__pyconfigfile = tempfile.NamedTemporaryFile(mode='w')
        confargs = ['--pyconfigfile', self.__pyconfigfile.name]

        self.__pyconfigfile.write('\n'.join(pyconf))
        self.__pyconfigfile.flush()

        super().__init__(exe='openheating-circuits.py',
                         busname=names.Bus.CIRCUITS,
                         args=confargs)

    def stop(self):
        self.__pyconfigfile.close()
        return super().stop()

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
