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
        # off if consumer's wanted_temperature reached.
        if self.__consumer.temperature() >= self.__consumer.wanted_temperature():
            if self.__pump.is_running():
                self.__pump.stop()
            self.__falling = True
            return

        # don't care if pump is on; leave it running.
        if self.__pump.is_running():
            return

        # consumer's temperature below wanted. are we falling? if so,
        # then we better wait until the temperature is below our
        # anti-oscillating threshold

        if not self.__falling:
            self.__falling = False
            self.__pump.start()
            return

        if self.__consumer.temperature() < self.__consumer.wanted_temperature() - self.__anti_oscillating_threshold:
            self.__pump.start()
            return
