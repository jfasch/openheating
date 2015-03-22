from openheating.testutils.file_switch import FileSwitch
from openheating.testutils.persistent_test import PersistentTestCase

import unittest
import logging

class FileSwitchTest(PersistentTestCase):
    def test__basic(self):
        switch_path = self.rootpath()+'/switch'
        open(switch_path, 'w').write('off\n')
        switch = FileSwitch(path=switch_path)
        
        # initial state: off, as I said above
        self.assertEqual(switch.get_state(), False)

        switch.set_state(True)
        self.assertEqual(open(switch_path).read(), 'on\n')
        
        switch.set_state(False)
        self.assertEqual(open(switch_path).read(), 'off\n')
        
        # see if he understands anything that looks like 'on', 'off'
        open(switch_path, 'w').write('off')
        self.assertEqual(switch.get_state(), False)
        open(switch_path, 'w').write('on')
        self.assertEqual(switch.get_state(), True)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FileSwitchTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite)
