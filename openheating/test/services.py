from . import testutils

from openheating.error import HeatingError
from openheating.dbus import dbusutil

import pydbus

import tempfile
import subprocess
import sys


def start(services):
    for s in services:
        s.start()

def stop(services):
    errors = []
    for s in services:
        try:
            s.stop()
        except Exception as e:
            errors.append(e)
    if len(errors) != 0:
        msg = ['there were errors while stopping services ...']
        for e in errors:
            msg.append(str(e))
        raise RuntimeError('\n'.join(msg))

class _Service:
    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__argv = [testutils.find_executable(exe), '--session']
        if args is not None:
            self.__argv += args
        self.__process = None

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
            print('STDERR >>>', file=sys.stderr)
            print(self.stderr, file=sys.stderr)
            print('STDERR <<<', file=sys.stderr)
            rc = self.__process.returncode
            self.__process = None

            raise HeatingError('start: name {} did not appear within timeout'.format(self.__busname))

    def stop(self):
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

        if self.__process.returncode != 0:
            print('STDERR >>>', file=sys.stderr)
            print(self.stderr, file=sys.stderr)
            print('STDERR <<<', file=sys.stderr)
            raise HeatingError('stop: service exited with status {}'.format(self.__process.returncode))

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

class ThermometerService(_Service):
    def __init__(self, ini):
        self.__ini = tempfile.NamedTemporaryFile(mode='w')
        self.__ini.write('\n'.join(ini))
        self.__ini.flush()

        super().__init__(exe='openheating-thermometers.py', busname=dbusutil.THERMOMETERS_BUSNAME,
                         args=['--configfile', self.__ini.name])

    def stop(self):
        super().stop()
        self.__ini.close()

class ErrorService(_Service):
    def __init__(self):
        super().__init__(
            exe='openheating-errors.py',
            busname=dbusutil.ERRORS_BUSNAME,
        )

class ExceptionTesterService(_Service):
    def __init__(self):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=dbusutil.EXCEPTIONTESTER_BUSNAME,
        )

class ManagedObjectTesterService(_Service):
    def __init__(self, stampdir):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=dbusutil.MANAGEDOBJECTTESTER_BUSNAME,
            args=['--stamp-directory', stampdir],
        )
