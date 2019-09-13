from openheating.thermometer_history import ThermometerHistory

import datetime
import unittest


class ThermometerHistoryTest(unittest.TestCase):
    def test__duration_sec(self):
        history = ThermometerHistory(interval=1, duration=5) # seconds
        history.new_sample(0,0)
        history.new_sample(1,1)
        history.new_sample(2,2)
        
        # interval is 1, so it must have recorded every sample
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], (2,2))
        self.assertEqual(history[1], (1,1))
        self.assertEqual(history[2], (0,0))

        # duration is 5, so we can insett another 2
        history.new_sample(3,3)
        history.new_sample(4,4)
        self.assertEqual(len(history), 5)

        # ... until the oldest start falling off at the tail
        history.new_sample(5,5)
        self.assertEqual(len(history), 6)
        self.assertEqual(history[0], (5,5))
        self.assertEqual(history[1], (4,4))
        self.assertEqual(history[2], (3,3))
        self.assertEqual(history[3], (2,2))
        self.assertEqual(history[4], (1,1))
        self.assertEqual(history[5], (0,0))

    def test__interval(self):
        history = ThermometerHistory(interval=2, duration=100)
        history.new_sample(1,1)
        history.new_sample(2,2)
        history.new_sample(3,3)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], (3,3))
        self.assertEqual(history[1], (1,1))

        history.new_sample(4,4)
        history.new_sample(5,5)
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], (5,5))
        self.assertEqual(history[1], (3,3))
        self.assertEqual(history[2], (1,1))
        
    def test__verify_ascending_time(self):
        history = ThermometerHistory(interval=1, duration=4)
        history.new_sample(2, 22)
        self.assertRaises(ThermometerHistory.TimeAscendingError, history.new_sample, 1, 21)

    def test__iter(self):
        history = ThermometerHistory(interval=1, duration=5)
        history.new_sample(1, 1)
        history.new_sample(2, 2)
        history.new_sample(3, 3)
        samples = [ (ts, temp) for ts, temp in history ]
        self.assertEqual(samples, [(3, 3), (2, 2), (1, 1)])

    def test_datetime(self):
        history = ThermometerHistory(
            interval=datetime.timedelta(minutes=15), 
            duration=datetime.timedelta(days=1))
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=1), 0)
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=1, minute=10), 0)
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=2), 0)

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], (datetime.datetime(year=2019, month=9, day=13, hour=2).timestamp(), 0))
        self.assertEqual(history[1], (datetime.datetime(year=2019, month=9, day=13, hour=1).timestamp(), 0))

    def test__cap_fractional_timestamps(self):
        history = ThermometerHistory(interval=1, duration=10)
        history.new_sample(1.2, 1)
        self.assertEqual(history[0], (1,1))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerHistoryTest)
