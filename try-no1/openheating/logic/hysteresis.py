class Hysteresis:
    def __init__(self, low, high):
        assert low < high

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

    def __str__(self):
        return '(%.1f,%.1f)' % (round(self.__low, 1), round(self.__high, 1))
