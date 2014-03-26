from .producer import Producer
from .consumer import Consumer
from .pump import Pump

class Transport:
    def __init__(self, producer, consumer, anti_oscillating_threshold, pump):
        assert isinstance(producer, Producer)
        assert isinstance(consumer, Consumer)
        assert isinstance(pump, Pump)
        
        self.__producer = producer
        self.__consumer = consumer
        self.__anti_oscillating_threshold = anti_oscillating_threshold
        self.__pump = pump

        # had we reached the consumer's wanted_temperature already
        # before? if so, we don't switch on the pump again unless we
        # see a consumer temperature below a restart_delay threshold
        # diff.
        self.__falling = False

    def move(self):
        if self.__consumer.temperature() >= self.__consumer.wanted_temperature():
            self.__pump.stop()
            self.__falling = True
            return

        if self.__producer.temperature() < self.__consumer.wanted_temperature():
            self.__producer.peek()

        if self.__producer.temperature() - 7 <= self.__consumer.temperature():
            self.__pump.stop()
            self.__falling = False
            return

        if not self.__falling:
            self.__pump.start()
            return

        # falling ...
        if self.__consumer.temperature() < self.__consumer.wanted_temperature() - self.__anti_oscillating_threshold:
            self.__pump.start()
            self.__falling = False
            return
