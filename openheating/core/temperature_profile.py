import itertools
import datetime


class TemperatureProfile:
    def __init__(self, thermometer):
        self.__thermometer = thermometer
        self.__idgen = itertools.count()
        self.__samples = []

    def pull_sample(self, timestamp):
        assert type(timestamp) is datetime.datetime
        temperature = self.__thermometer.get_temperature()
        sample_id = next(self.__idgen)
        self.__samples.append((sample_id, timestamp, temperature))

    def get_samples(self):
        return self.__samples
