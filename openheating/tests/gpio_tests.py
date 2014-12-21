import openheating.gpio as gpio

import unittest
import logging

class GPIOTest(unittest.TestCase):
    def test__basic(self):
        io = gpio.create(4)
        io.set_direction(gpio.IN)
        io.set_value(1)
        self.assertEqual(io.get_value(), 1)

        # we use __del__ to unexport the gpio. see if that works.
        del io
        gpio.create(4)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GPIOTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
