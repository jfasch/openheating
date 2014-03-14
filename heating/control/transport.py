class Transport:
    def __init__(self, producer, consumer, pump):
        self.__producer = producer
        self.__consumer = consumer
        self.__pump = pump

    def move(self):
        if self.__consumer.temperature() >= self.__consumer.wanted_temperature():
            if self.__pump.is_running():
                self.__pump.stop()
        else:
            if not self.__pump.is_running():
                self.__pump.start()
 
