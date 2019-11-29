from .hysteresis import Hysteresis
from .error import ClockSkewError
from . import timeutil


class Circuit:
    def __init__(self, pump, producer, consumer, diff_low, diff_high):
        self.__pump = pump
        self.__producer = producer
        self.__consumer = consumer
        self.__hysteresis = Hysteresis(low=diff_low, high=diff_high, 
                                       below_low=lambda:self.__pump.set_state(False),
                                       above_high=lambda:self.__pump.set_state(True))
        self.__active = False
        self.__last_ts = None

    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def is_active(self):
        return self.__active

    def look(self, timestamp):
        if not self.__active:
            return

        timestamp = timeutil.dt2unix(timestamp)

        if self.__last_ts is not None:
            if timestamp < self.__last_ts:
                raise ClockSkewError()
        self.__last_ts = timestamp

        tprod = self.__producer.get_temperature()
        tcons = self.__consumer.get_temperature()
        self.__hysteresis.add_sample(timestamp, tprod-tcons)
