from openheating.dbus import dbusutil
from openheating.dbus.util import lifecycle
from openheating.test import testutils
from openheating.test import services

from gi.repository import GLib

import unittest
import tempfile
import time
import signal
import os.path


class ManagedTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.__directory = tempfile.TemporaryDirectory()
    def tearDown(self):
        self.__directory.cleanup()
        
    def test__basic(self):
        self.start_services([services.ManagedObjectTesterService(stampdir=self.__directory.name)])
        self.stop_services()
        self.assertTrue(os.path.isfile(self.__directory.name+'/started'))
        self.assertTrue(os.path.isfile(self.__directory.name+'/stopped'))

class GracefulTerminationTest(unittest.TestCase):
    def setUp(self):
        self.__loop = GLib.MainLoop()
        self.__gt = lifecycle.GracefulTermination(self.__loop, (signal.SIGUSR1,))
        self.__gt.install()
    def tearDown(self):
        self.__gt.uninstall()

        # signal handler cleanup done?
        self.assertEqual(signal.getsignal(signal.SIGUSR1), signal.SIG_DFL)

    def test__signal_arrives_while_loop_runs(self):
        '''request termination while the loop is running.'''

        def send_signal():
            os.kill(os.getpid(), signal.SIGUSR1)
            return False # dont re-arm timer
        GLib.timeout_add(1, # milliseconds
                         send_signal)

        signal.alarm(5)
        self.__loop.run()
        signal.alarm(0)

    def test__signal_arrives_before_loop_runs(self):
        '''request termination before the loop is running'''

        os.kill(os.getpid(), signal.SIGUSR1)
        for _ in range(20):
            if self.__gt.requested: break
            time.sleep(0.1)
        else:
            self.fail('signal handler timeout')

        signal.alarm(5)
        self.__loop.run()
        signal.alarm(0)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ManagedTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GracefulTerminationTest))

if __name__ == '__main__':
    testutils.run(suite)
