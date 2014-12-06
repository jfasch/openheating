class Hysteresis:
    def __init__(self, low, high):
        self.__low = low
        self.__high = high
    def above(self, value):
        return value > self.__high
    def below(self, value):
        return value < self.__low
