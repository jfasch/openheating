import logging


class Hysteresis:
    def __init__(self, name, low, high, below_low, above_high):
        self.__name = name
        self.__low = low
        self.__high = high
        self.__below_low = below_low
        self.__above_high = above_high

    def __call__(self, timestamp, value):
        return self.add_sample(timestamp, value)

    def add_sample(self, timestamp, value):
        if value < self.__low:
            logging.debug('{}: {} is below low (<{})'.format(self.__name, value, self.__low))
            self.__below_low()
        elif value > self.__high:
            logging.debug('{}: {} is above high (>{})'.format(self.__name, value, self.__high))
            self.__above_high()
