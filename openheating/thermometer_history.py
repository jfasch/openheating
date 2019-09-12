from .error import HeatingError


class ThermometerHistory:
    class TimeAscendingError(HeatingError):
        def __init__(self, new, previous):
            super().__init__(
                msg='New timestamp {new} is before previous timestamp {previous}'
                .format(new=new, previous=previous))

    def __init__(self, maxvalues):
        self.__maxvalues = maxvalues
        self.__samples = []

    def __len__(self):
        return len(self.__samples)

    def __getitem__(self, index):
        return self.__samples[index]

    def new_sample(self, timestamp, temperature):
        if len(self.__samples) > 0:
            previous, _ = self.__samples[0]
            if timestamp < previous:
                raise self.TimeAscendingError(new=timestamp, previous=previous)

        self.__samples.insert(0, (timestamp, temperature))
        if len(self.__samples) > self.__maxvalues:
            del self.__samples[-1]

    def cutout(self, youngest, oldest):
        ret = []
        for timestamp, temperature in self.__samples:
            if oldest <= timestamp <= youngest:
                ret.append((timestamp, temperature))
        return ret
