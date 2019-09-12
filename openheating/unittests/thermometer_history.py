from openheating.thermometer_history import ThermometerHistory

import unittest


class ThermometerHistoryTest(unittest.TestCase):
    def test__basic(self):
        history = ThermometerHistory(maxvalues=2)
        history.new_sample(1, 21)
        history.new_sample(2, 22)

        self.assertEqual(len(history), 2)

        ts, temp = history[0]
        self.assertEqual(ts, 2)
        self.assertEqual(temp, 22)

        ts, temp = history[1]
        self.assertEqual(ts, 1)
        self.assertEqual(temp, 21)

        # add one more sample; the oldest is removed and the indexes
        # advance

        history.new_sample(3, 23)

        self.assertEqual(len(history), 2)

        ts, temp = history[0]
        self.assertEqual(ts, 3)
        self.assertEqual(temp, 23)

        ts, temp = history[1]
        self.assertEqual(ts, 2)
        self.assertEqual(temp, 22)

    def test__verify_ascending_time(self):
        history = ThermometerHistory(maxvalues=2)
        history.new_sample(2, 22)
        self.assertRaises(ThermometerHistory.TimeAscendingError, history.new_sample, 1, 21)

    def test__all(self):
        history = ThermometerHistory(maxvalues=100)
        history.new_sample(1, 1)
        history.new_sample(2, 2)
        history.new_sample(3, 3)
        history.new_sample(4, 4)
        history.new_sample(5, 5)
        history.new_sample(6, 6)

        samples = history.all()
        self.assertEqual(len(samples), 6)
        self.assertEqual(cutout[0], (6,6))
        self.assertEqual(cutout[1], (5,5))
        self.assertEqual(cutout[2], (4,4))
        self.assertEqual(cutout[3], (3,3))
        self.assertEqual(cutout[4], (2,2))
        self.assertEqual(cutout[5], (1,1))

    def test__cutout(self):
        history = ThermometerHistory(maxvalues=100)
        history.new_sample(1, 1)
        history.new_sample(2, 2)
        history.new_sample(3, 3)
        history.new_sample(4, 4)
        history.new_sample(5, 5)
        history.new_sample(6, 6)

        cutout = history.cutout(youngest=6, oldest=2)
        self.assertEqual(len(cutout), 5)
        self.assertEqual(cutout[0], (6,6))
        self.assertEqual(cutout[1], (5,5))
        self.assertEqual(cutout[2], (4,4))
        self.assertEqual(cutout[3], (3,3))
        self.assertEqual(cutout[4], (2,2))

        cutout = history.cutout(youngest=100, oldest=2)
        self.assertEqual(len(cutout), 5)
        self.assertEqual(cutout[0], (6,6))
        self.assertEqual(cutout[1], (5,5))
        self.assertEqual(cutout[2], (4,4))
        self.assertEqual(cutout[3], (3,3))
        self.assertEqual(cutout[4], (2,2))

        cutout = history.cutout(youngest=6, oldest=0)
        self.assertEqual(len(cutout), 6)
        self.assertEqual(cutout[0], (6,6))
        self.assertEqual(cutout[1], (5,5))
        self.assertEqual(cutout[2], (4,4))
        self.assertEqual(cutout[3], (3,3))
        self.assertEqual(cutout[4], (2,2))

        self.assertEqual(cutout[5], (1,1))
        
suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerHistoryTest)
