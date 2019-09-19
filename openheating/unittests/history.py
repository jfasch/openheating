from openheating.history import History

import time
import datetime
import unittest

import os
import os.path


class HistoryTest(unittest.TestCase):

    def test__oldestfirst(self):
        history = History()
        history.add(0, 0)
        history.add(1, 0)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], (0,0))
        self.assertEqual(history[1], (1,0))

    def test__duration_nosamples(self):
        history = History(duration=10)
        history.add(0, 0)
        self.assertEqual(len(history), 1)
        history.add(1, 0)
        self.assertEqual(len(history), 2)
        # 0..10 is still within duration=10
        history.add(10, 0)
        # 11 pushes 0 out
        history.add(11, 0)
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0][0], 1)
        self.assertEqual(history[1][0], 10)
        self.assertEqual(history[2][0], 11)

    def test__duration_samples(self):
        history = History(duration=10, samples=((ts,0) for ts in range(12)))
        self.assertEqual(len(history), 11)
        self.assertEqual(history[0][0], 1)
        self.assertEqual(history[1][0], 2)
        # ... etc ...
        self.assertEqual(history[10][0], 11)

    def test__verify_ascending_time(self):
        history = History()
        history.add(2, 0)
        self.assertRaises(History.TimeAscendingError, history.add, 1, 0)

    def test__iter(self):
        history = History()
        history.add(1, 1)
        history.add(2, 2)
        history.add(3, 3)
        samples = [ (ts, temp) for ts, temp in history ]
        self.assertEqual(samples, [(1, 1), (2, 2), (3, 3), ])
        samples = list(history)
        self.assertEqual(samples, [(1, 1), (2, 2), (3, 3), ])

    def test__cap_fractional_timestamps(self):
        history = History()
        history.add(1.2, 1)
        self.assertEqual(history[0], (1,1))

    def test__distill(self):
        minute = History(unchecked_samples=((ts,0) for ts in range(60)))
        half_minute = minute.distill(granularity=5, duration=30)

        # duration
        self.assertLessEqual(half_minute[0][0] - half_minute[-1][0], 30)

        # granularity
        prev = None
        for ts, _ in half_minute:
            if prev is None: continue
            self.assertLessEqual(ts - prev, 5)
            prev = ts

    def test__duration_in_datetime(self):
        history = History(duration=datetime.timedelta(seconds=30))
        history.add(1,0)
        history.add(2,0)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(HistoryTest)

if __name__ == '__main__':
    unittest.main()
