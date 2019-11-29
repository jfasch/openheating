from .hysteresis import Hysteresis
from .error import ClockSkewError
from . import timeutil

import logging


class Circuit:
    def __init__(self, name, pump, producer, consumer, diff_low, diff_high):
        self.__name = name
        self.__pump = pump
        self.__producer = producer
        self.__consumer = consumer
        self.__diff_hysteresis = Hysteresis(
            name='Hysteresis({})'.format(name),
            low=diff_low,
            high=diff_high,
            below_low=self.__pump_off,
            above_high=self.__pump_on)
        self.__active = False
        self.__last_ts = None

    def activate(self):
        if not self.__active:
            logging.debug('{}: activated'.format(self.__name))
            self.__active = True

    def deactivate(self):
        if self.__active:
            logging.debug('{}: deactivated'.format(self.__name))
            self.__active = False

    def is_active(self):
        return self.__active

    def poll(self, timestamp):
        if not self.__active:
            return

        timestamp = timeutil.dt2unix(timestamp)

        if self.__last_ts is not None:
            if timestamp < self.__last_ts:
                raise ClockSkewError()
        self.__last_ts = timestamp

        tprod = self.__producer.get_temperature()
        tcons = self.__consumer.get_temperature()
        logging.debug('{}: producer {}, consumer {}, diff {}'.format(self.__name, tprod, tcons, tprod-tcons))

        self.__diff_hysteresis.add_sample(timestamp, tprod-tcons)

    def __pump_on(self):
        if not self.__pump.get_state():
            logging.debug('{}: pump {} on'.format(self.__name, self.__pump.get_name()))
            self.__pump.set_state(True)

    def __pump_off(self):
        if self.__pump.get_state():
            logging.debug('{}: pump {} off'.format(self.__name, self.__pump.get_name()))
            self.__pump.set_state(False)
