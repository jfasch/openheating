from . import testutils

from openheating.error import HeatingError
from openheating.dbus import dbusutil

import tempfile
import subprocess


class _Service:
    def __init__(self, busname, exe, args=None, popenargs=None):
        self.__busname = busname
        argv = [testutils.find_executable(exe), '--session']
        if args is not None:
            argv += args
        kwargs = popenargs and popenargs or {}
        self.__process = subprocess.Popen(argv, **kwargs)

        # wait until busname appears
        subprocess.run(
            ['gdbus', 'wait', '--session', busname, '--timeout', '10'],
            check=True,
        )

    def stop(self):
        self.__process.terminate()
        # our services mess with signals a bit (graceful eventloop
        # termination), so apply a timeout in case anything goes
        # wrong.
        self.__process.wait(timeout=5) 

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
            # pydbus server logs any exceptions to default logger, on
            # stderr
            popenargs={'stderr': subprocess.DEVNULL},
        )

        
