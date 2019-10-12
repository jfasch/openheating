from . import testutils

from openheating.dbus import dbusutil

import tempfile
import subprocess


class ThermometerService:
    def __init__(self, ini):
        self.__ini = tempfile.NamedTemporaryFile(mode='w')
        self.__ini.write('\n'.join(ini))
        self.__ini.flush()

        self.__process = subprocess.Popen([
            testutils.find_executable('openheating-thermometers.py'),
            '--session',
            '--configfile', self.__ini.name,
        ])

        # wait until busname appears
        completed_process = subprocess.run(
            ['gdbus', 'wait', '--session', dbusutil.THERMOMETERS_BUSNAME, '--timeout', '10'],
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

        self.__ini.close()

        # wait for busname to disappear
        for _ in range(10):
            completed_process = subprocess.run(
                ['gdbus', 'call', '--session', '--dest', 'org.freedesktop.DBus',
                 '--object-path', '/org/freedesktop/DBus', '--method', 'org.freedesktop.DBus.ListNames'],
                stdout=subprocess.PIPE,
                check=True,
            )
            names = eval(completed_process.stdout)
            
            if dbusutil.THERMOMETERS_BUSNAME in names:
                time.sleep(0.5)
                continue
            else:
                break
        else:
            self.fail('{} still on the bus'.format(dbusutil.THERMOMETERS_BUSNAME))
        
