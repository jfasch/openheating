from openheating.pidfile import PIDFile
from openheating.testutils import PersistentTestCase

import unittest
import os
import sys
import os.path

class DaemonTest(PersistentTestCase):
    def test__pidfile(self):
        try:
            filename = self.rootpath()+'/pidfile'
            pid = os.fork()
            if pid == 0:
                pf = PIDFile(filename=filename, main_pid=os.getpid())
                sys.exit(0)
            else:
                os.waitpid(pid, 0)
            self.failIf(os.path.exists(filename))
        except SystemExit: pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DaemonTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
