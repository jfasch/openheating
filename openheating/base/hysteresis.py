class Hysteresis:
    def __init__(self, low, high, below_low, above_high):
        self.__low = low
        self.__high = high
        self.__below_low = below_low
        self.__above_high = above_high

    def add_sample(self, timestamp, value):
        if value < self.__low:
            self.__below_low()
        elif value > self.__high:
            self.__above_high()
