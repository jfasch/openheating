from .source import Source

class PassiveSource(Source):
    def __init__(self, name, thermometer):
        Source.__init__(self, name)
        self.__thermometer = thermometer

    def temperature(self):
        return self.__thermometer.temperature()

    def do_request(self):
        pass
    def do_release(self):
        pass
