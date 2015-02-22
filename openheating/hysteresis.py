class Hysteresis:
    def __init__(self, low, high):
        self.__low = low
        self.__high = high

    def low(self):
        return self.__low
    def high(self):
        return self.__high

    def above(self, value):
        return value > self.__high
    def below(self, value):
        return value < self.__low
    def between(self, value):
        return self.__low <= value <= self.__high
