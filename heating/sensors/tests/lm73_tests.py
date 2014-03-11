from heating.sensors.lm73 import LM73

import unittest

class LM73_Tests(unittest.TestCase):
    def testBasic(self):
        sensor = LM73(simulated_temperature=1.234, simulated_resolution=LM73.RES0_25)
        self.failUnlessAlmostEqual(sensor.get_temperature(), 1.234, 3)

        sensor.set_resolution(LM73.RES0_125)
        sensor.set_temperature(2.345)
        self.failUnlessAlmostEqual(sensor.get_temperature(), 2.345, 3)

        sensor.set_resolution(LM73.RES0_0625)
        sensor.set_temperature(3.456)
        self.failUnlessAlmostEqual(sensor.get_temperature(), 3.456, 3)

        sensor.set_resolution(LM73.RES0_03125)
        sensor.set_temperature(4.567)
        self.failUnlessAlmostEqual(sensor.get_temperature(), 4.567, 3)
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LM73_Tests))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
