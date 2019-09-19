from .error import HeatingError

import datetime
import time
from bisect import bisect_left
from collections import deque


def _delta2unix(delta):
    try:
        num = delta.total_seconds()
    except AttributeError: # assume number
        num = delta
    # cap fractional timestamps to entire seconds
    return int(num)


class History:
    class TimeAscendingError(HeatingError):
        def __init__(self, new, previous):
            super().__init__(
                msg='New timestamp {new} is before previous timestamp {previous}'
                .format(new=new, previous=previous))

    def __init__(self, duration=None, samples=None, unchecked_samples=None):
        assert not (unchecked_samples and samples)

        self.__duration = duration

        if unchecked_samples:
            self.__samples = deque(unchecked_samples)
            return

        self.__samples = deque()
        if samples:
            for ts, v in samples:
                self.add(ts,v)

    def __len__(self):
        return len(self.__samples)

    def __iter__(self):
        yield from self.__samples

    def __getitem__(self, index):
        return self.__samples[index]

    def add(self, timestamp, value):
        timestamp = int(timestamp) # cap fractional timestamps
        if len(self.__samples):
            previous = self.__samples[-1][0]
            if timestamp < previous:
                raise self.TimeAscendingError(new=timestamp, previous=previous)

            if self.__duration is not None:
                oldest = self.__samples[0][0]
                if timestamp - oldest > self.__duration:
                    del self.__samples[0]

        self.__samples.append((timestamp, value))

    def distill(self, granularity, duration):
        granularity = _delta2unix(granularity)
        duration = _delta2unix(duration)

        if len(self.__samples) == 0:
            return History()

        youngest_ts = self.__samples[-1][0]
        boundary_ts = youngest_ts - duration
        if boundary_ts < 0:
            boundary_ts = 0

        # search boundary index
        boundary_idx = 0
        while self.__samples[boundary_idx][0] < boundary_ts:
            boundary_idx += 1

        distilled = []
        last_ts = boundary_ts
        cur_idx = boundary_idx
        while cur_idx < len(self.__samples):
            if self.__samples[cur_idx][0] - last_ts >= granularity:
                distilled.append(self.__samples[cur_idx])
            cur_idx += 1

        return History(unchecked_samples=distilled)
