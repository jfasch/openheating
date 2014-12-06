class Source:
    def __init__(self, name, thermometer):
        self.__name = name
        self.__thermometer = thermometer
        self.__requesters = set()

    def temperature(self):
        return self.__thermometer.temperature()

    def request(self, sink):
        self.__requesters.add(sink)

    def release(self, sink):
        self.__requesters.discard(sink)

    def requesters(self):
        return self.__requesters
