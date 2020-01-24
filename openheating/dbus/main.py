from . import interface_repo
from . import node
from . import lifecycle
from . import names
from .pollable_client import Pollable_Client

import logging


class MainPollable_Client(Pollable_Client):
    def __init__(self, bus):
        super().__init__(bus=bus, busname=names.Bus.MAIN, path='/')


@node.Definition(interfaces=interface_repo.get(interface_repo.POLLABLE))
class Main_Server:
    def __init__(self, bus, services):
        self.__bus = bus
        self.__services = services

    def poll(self, timestamp):
        logging.debug('poll, timestamp {}'.format(timestamp))
        for s in self.__services:
            s.poll(self.__bus, timestamp)
