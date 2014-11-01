from ..pump import Pump

class TestPump(Pump):
    def __init__(self, running):
        assert type(running) is bool
        self.__is_running = running
    def is_running(self):
        return self.__is_running
    def start(self):
        self.__is_running = True
    def stop(self):
        self.__is_running = False

