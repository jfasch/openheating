from . import testutils

from openheating.error import HeatingError
from openheating.dbus import dbusutil

import tempfile
import subprocess
import sys


class _Service:
    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__argv = [testutils.find_executable(exe), '--session']
        if args is not None:
            self.__argv += args
        self.__process = None

    def start(self, suppress_stderr=True):
        if suppress_stderr:
            kwargs = {'stderr': subprocess.DEVNULL}
        else:
            kwargs = {}

        self.__process = subprocess.Popen(self.__argv, **kwargs)

        # wait until busname appears
        subprocess.run(
            ['gdbus', 'wait', '--session', self.__busname, '--timeout', '10'],
            check=True,
        )

    def stop(self):
        assert self.__process is not None

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

        if self.__process.returncode != 0:
            raise HeatingError('service exited with status {}'.format(self.__process.returncode))

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

        
