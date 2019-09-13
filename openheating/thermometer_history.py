from .error import HeatingError

import datetime


class ThermometerHistory:
    class TimeAscendingError(HeatingError):
        def __init__(self, new, previous):
            super().__init__(
                msg='New timestamp {new} is before previous timestamp {previous}'
                .format(new=new, previous=previous))

    def __init__(self, interval, duration):
        try:
            self.__interval = interval.total_seconds()
        except AttributeError: # assume number
            self.__interval = interval

        try:
            self.__duration = duration.total_seconds()
        except AttributeError: # assume number
            self.__duration = duration

        self.__samples = []

    def __len__(self):
        return len(self.__samples)

    def __iter__(self):
        yield from self.__samples

    def __getitem__(self, index):
        return self.__samples[index]

    def new_sample(self, timestamp, temperature):
        try:
            timestamp = timestamp.timestamp()
        except AttributeError:
            pass

        # cap fractional timestamps to entire seconds
        timestamp = int(timestamp)

        if len(self.__samples):
            previous, _ = self.__samples[0]
            if timestamp < previous:
                raise self.TimeAscendingError(new=timestamp, previous=previous)
            if timestamp - previous < self.__interval:
                return

            oldest, _ = self.__samples[-1]
            if oldest - timestamp > self.__duration:
                del self.__samples[-1]

        self.__samples.insert(0, (timestamp, temperature))
