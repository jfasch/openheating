from .polled import Polled

import logging

class Producer(Polled):
    def __init__(self, name, backend, overheat_temperature, alarm_switch):
        self.__name = name
        self.__backend = backend
        self.__overheat_temperature = overheat_temperature
        self.__alarm_switch = alarm_switch

        # transports I am attached to. they register themselves once
        # they get to know me.
        self.__transports = set()

        # transports who want me to heat up.
        self.__acquirers = set()

        self.__alarm_switch.off()

    def add_transport(self, transport):
        ''' Called by Transport, when initialized with self as Producer '''
        assert not transport in self.__transports
        self.__transports.add(transport)

    def get_transports(self):
        ''' For testing only, irrelevant in real life '''
        return self.__transports
        
    def temperature(self):
        return self.__backend.temperature()

    def acquire(self, name):
        num_before = len(self.__acquirers)
        self.__acquirers.add(name)
        if num_before == 0 and len(self.__acquirers) > 0:
            self.__backend.start_producing()

    def release(self, name):
        num_before = len(self.__acquirers)
        self.__acquirers.discard(name)
        if num_before > 0 and len(self.__acquirers) == 0:
            self.__backend.stop_producing()

    def is_acquired(self):
        return len(self.__acquirers) > 0

    def get_acquirers(self):
        ''' For testing only, irrelevant in real life '''
        return self.__acquirers

    def needs_cooling(self):
        return self.__backend.temperature() >= self.__overheat_temperature

    def poll(self):
        # see if we are overheating. if we do, and we are not already
        # being cooled, call out to our transports for cooling. alarm
        # if necessary.

        if not self.needs_cooling():
            return

        for t in self.__transports:
            t.producer_needs_cooling()

        n_coolers = 0
        for t in self.__transports:
            if t.is_running():
                n_coolers += 1

        self.__debug("%d out of %d transports give cooling" % (n_coolers, len(self.__transports)))

        if n_coolers == 0:
            self.__alarm_switch.on()
        else:
            self.__alarm_switch.off()
           
    def __debug(self, msg):
        logging.debug('%s: %s' % (self.__name, msg))
