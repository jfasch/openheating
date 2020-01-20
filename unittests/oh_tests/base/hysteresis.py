from openheating.base.hysteresis import Hysteresis

import unittest


class HysteresisTest(unittest.TestCase):

    def test__basic(self):
        n_above_high = n_below_low = 0
        def above(): 
            nonlocal n_above_high
            n_above_high += 1
        def below(): 
            nonlocal n_below_low
            n_below_low += 1

        hy = Hysteresis(debugstr='blah', low=20, high=25, 
                        below_low=below, above_high=above)

        # below
        hy.add_sample(0, 12.2)
        self.assertEqual(n_below_low, 1)
        self.assertEqual(n_above_high, 0)

        # between
        hy.add_sample(1, 20.1)
        self.assertEqual(n_below_low, 1)
        self.assertEqual(n_above_high, 0)

        # above
        hy.add_sample(1, 26.9)
        self.assertEqual(n_below_low, 1)
        self.assertEqual(n_above_high, 1)

        # above
        hy.add_sample(1, 27.1)
        self.assertEqual(n_below_low, 1)
        self.assertEqual(n_above_high, 2)

        # between
        hy.add_sample(1, 24.3)
        self.assertEqual(n_below_low, 1)
        self.assertEqual(n_above_high, 2)

        # below
        hy.add_sample(1, 19.2)
        self.assertEqual(n_below_low, 2)
        self.assertEqual(n_above_high, 2)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(HysteresisTest)

if __name__ == '__main__':
    unittest.main()
