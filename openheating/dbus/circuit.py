from . import node
from . import error
from . import interface_repo

from ..base.circuit import Circuit
from ..base import timeutil

import logging


class Circuit_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

        # cached attributes
        self.__name = self.__description = None
        
    @error.maperror
    def get_name(self):
        if self.__name is None:
            self.__name = self.__proxy.get_name()
        return self.__name
        
    @error.maperror
    def get_description(self):
        if self.__description is None:
            self.__description = self.__proxy.get_description()
        return self.__description

    @error.maperror
    def activate(self):
        self.__proxy.activate()

    @error.maperror
    def deactivate(self):
        return self.__proxy.deactivate()

    @error.maperror
    def is_active(self):
        return self.__proxy.is_active()

    @error.maperror
    def get_producer_temperature(self):
        return self.__proxy.get_producer_temperature()

    @error.maperror
    def get_consumer_temperature(self):
        return self.__proxy.get_consumer_temperature()

    @error.maperror
    def poll(self, timestamp):
        return self.__proxy.poll(timestamp)

@node.Definition(interfaces=interface_repo.get(
    interface_repo.CIRCUIT,
    interface_repo.POLLABLE))
class Circuit_Server:
    def __init__(self, name, description, circuit):
        self.__name = name
        self.__description = description
        self.__circuit = circuit
        self.__logger = logging.getLogger(self.__name)

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def activate(self):
        self.__logger.debug('activate')
        return self.__circuit.activate()

    def deactivate(self):
        self.__logger.debug('deactivate')
        return self.__circuit.deactivate()

    def is_active(self):
        return self.__circuit.is_active()

    def get_producer_temperature(self):
        return self.__circuit.producer_thermometer.get_temperature()

    def get_consumer_temperature(self):
        return self.__circuit.consumer_thermometer.get_temperature()

    def poll(self, timestamp):
        self.__logger.debug('poll, ts={}({})'.format(timestamp, timeutil.unix2dt(timestamp)))
        return self.__circuit.poll(timestamp)
