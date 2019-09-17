from openheating.history import History

import datetime
import unittest

import os
import os.path


class HistoryTest(unittest.TestCase):
    def test__duration_sec(self):
        history = History(granularity=1, duration=5) # seconds
        history.new_sample(0,0)
        history.new_sample(1,1)
        history.new_sample(2,2)
        
        # granularity is 1, so it must have recorded every sample
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], (2,2))
        self.assertEqual(history[1], (1,1))
        self.assertEqual(history[2], (0,0))

        # duration is 5, so we can insert another 2
        history.new_sample(3,3)
        history.new_sample(4,4)
        self.assertEqual(len(history), 5)

        # another one. we treat duration as inclusive boundaries. this
        # means that we can insert ts=5 and ts=0 does not yet fall off
        # the end.
        history.new_sample(5,5)
        self.assertEqual(len(history), 6)
        self.assertEqual(history[0], (5,5))
        self.assertEqual(history[1], (4,4))
        self.assertEqual(history[2], (3,3))
        self.assertEqual(history[3], (2,2))
        self.assertEqual(history[4], (1,1))
        self.assertEqual(history[5], (0,0))

        # ts=6 will push ts=0 off the end
        history.new_sample(6,6)
        self.assertEqual(len(history), 6)
        self.assertEqual(history[0], (6,6))
        self.assertEqual(history[1], (5,5))
        self.assertEqual(history[2], (4,4))
        self.assertEqual(history[3], (3,3))
        self.assertEqual(history[4], (2,2))
        self.assertEqual(history[5], (1,1))

    def test__granularity(self):
        history = History(granularity=2, duration=100)
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
        history = History(granularity=1, duration=4)
        history.new_sample(2, 22)
        self.assertRaises(History.TimeAscendingError, history.new_sample, 1, 21)

    def test__iter(self):
        history = History(granularity=1, duration=5)
        history.new_sample(1, 1)
        history.new_sample(2, 2)
        history.new_sample(3, 3)
        samples = [ (ts, temp) for ts, temp in history ]
        self.assertEqual(samples, [(3, 3), (2, 2), (1, 1)])

    def test__datetime(self):
        history = History(
            granularity=datetime.timedelta(minutes=15), 
            duration=datetime.timedelta(days=1))
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=1), 0)
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=1, minute=10), 0)
        history.new_sample(datetime.datetime(year=2019, month=9, day=13, hour=2), 0)

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], (datetime.datetime(year=2019, month=9, day=13, hour=2).timestamp(), 0))
        self.assertEqual(history[1], (datetime.datetime(year=2019, month=9, day=13, hour=1).timestamp(), 0))

    def test__mixed_datetime(self):
        history = History(
            granularity=1, 
            duration=datetime.timedelta(hours=1))
        history.new_sample(0, 0)
        history.new_sample(30*60, 0)
        history.new_sample(60*60, 0)
        history.new_sample(60*60+1, 0)

        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], (60*60+1, 0))
        self.assertEqual(history[1], (60*60, 0))
        self.assertEqual(history[2], (30*60, 0))

    def test__cap_fractional_timestamps(self):
        history = History(granularity=1, duration=10)
        history.new_sample(1.2, 1)
        self.assertEqual(history[0], (1,1))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(HistoryTest)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    runner.run(suite)
