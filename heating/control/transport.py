from .producer import Producer
from .consumer import Consumer
from .pump import Pump

import logging

class Transport:

    def __init__(self,
                 name,
                 producer,
                 consumer, range_low, range_high,
                 pump,
                 alarm_switch):
        assert isinstance(producer, Producer)
        assert isinstance(consumer, Consumer)
        assert isinstance(pump, Pump)

        self.__name = name
        self.__producer = producer
        self.__consumer = consumer
        self.__pump = pump
        self.__alarm_switch = alarm_switch

        self.__round = 0

        self.__range_low = range_low
        self.__range_high = range_high

        self.__pump_running = False
        self.__pump.stop()

        self.__alarm_switch.off()

    def move(self):
        self.__round += 1
        
        if self.__pump_running:
            # handle emergency condition where producer is about to
            # explode
            if self.__producer.needs_cooling():
                if self.__pumping_pays_off():
                    self.__debug('producer needs cooling, leave pump running')
                else:
                    self.__debug('producer needs cooling, but cannot')
                    self.__stop_pump()
                    self.__alarm_switch.on()
                return
            self.__alarm_switch.off()

            # stop if consumer is satisfied (is at the high end of its
            # range)
            if self.__consumer.temperature() >= self.__consumer.wanted_temperature() + self.__range_high:
                self.__debug('consumer satisfied, switching pump off')
                self.__stop_pump()
                self.__producer.release(self.__name)
                return
            # producer is out of temperature, stop
            if not self.__pumping_pays_off():
                self.__debug('producer out of temperature')
                self.__stop_pump()
                self.__producer.acquire(self.__name)
                return
            self.__debug('keep on pumping')

        else: # pump not running
            # handle emergency condition where producer is about to
            # explode
            if self.__producer.needs_cooling():
                if self.__pumping_pays_off():
                    self.__debug('producer needs cooling, switch on pump')
                    self.__start_pump()
                else:
                    self.__debug('producer needs cooling, but cannot')
                    self.__alarm_switch.on()
                return
            self.__alarm_switch.off()
            
            if self.__consumer.temperature() >= self.__consumer.wanted_temperature() + self.__range_high:
                self.__debug('consumer satisfied, leaving pump off')
                return

            # consumer temperature below wanted. we can be certain
            # that we will need temperature soon - peek producer.
            if self.__producer.temperature() < self.__consumer.wanted_temperature():
                self.__debug('peek producer')
                self.__producer.acquire(self.__name)

            # consumer has fallen below watermark, see if we can do
            # someting
            if self.__consumer.temperature() <= self.__consumer.wanted_temperature() - self.__range_low:
                if not self.__pumping_pays_off():
                    self.__debug('pumping does not pay off, leaving pump alone')
                else:
                    self.__debug('switching on pump')
                    self.__start_pump()

    def __pumping_pays_off(self):
        return self.__producer.temperature() >= self.__consumer.temperature() + 5
                    
    def __start_pump(self):
        self.__pump.start()
        self.__pump_running = True

    def __stop_pump(self):
        self.__pump.stop()
        self.__pump_running = False

    def __debug(self, msg):
        logging.debug('%s(%d): %s' % (self.__name, self.__round, msg))
