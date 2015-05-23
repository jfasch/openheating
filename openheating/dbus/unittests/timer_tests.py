from .dbus_testcase import DBusTestCase

import unittest


class TimerTest(DBusTestCase):
    def test__basic(self):
        pass

        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TimerTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
