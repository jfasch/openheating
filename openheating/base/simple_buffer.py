from openheating.base.hysteresis import Hysteresis

import logging


class SimpleBuffer:
    def __init__(self, name, thermometer, circuit, low, high):
        self.__name = name
        self.__satisfied = True   # initially quiet
        self.__thermometer = thermometer
        self.__circuit = circuit

        self.__hysteresis = Hysteresis(
            debugstr='Hysteresis({})'.format(name),
            low=low,
            high=high,
            below_low=self._dont_be_satisfied,
            above_high=self._be_satisfied)

    def is_satisfied(self):
        return self.__satisfied

    def poll(self, timestamp):
        logging.debug('{}: poll({})'.format(self.__name, timestamp))

        self.__hysteresis(timestamp, self.__thermometer.get_temperature())

        if self.__satisfied:
            self.__circuit.deactivate()
        else:
            self.__circuit.activate()

    def _be_satisfied(self):
        if not self.__satisfied:
            logging.debug('{}: now satisfied'.format(self.__name))
            self.__satisfied = True

    def _dont_be_satisfied(self):
        if self.__satisfied:
            logging.debug('{}: not anymore satisfied'.format(self.__name))
            self.__satisfied = False

