from . import interface_repo
from . import node
from . import lifecycle
from . import names
from .pollable_client import Pollable_Client

from ..base import timeutil

from gi.repository import GLib

import logging


class MainPollable_Client(Pollable_Client):
    def __init__(self, bus):
        super().__init__(bus=bus, busname=names.Bus.MAIN, path='/')


@lifecycle.managed(startup='_startup', shutdown='_shutdown')
@node.Definition(interfaces=interface_repo.get(interface_repo.POLLABLE))
class Main_Server:
    def __init__(self, bus, services, interval):
        self.__bus = bus
        self.__services = services
        self.__poll_interval = interval
        self.__poll_timer_tag = None   # valid after _startup()

    def poll(self, timestamp):
        logging.debug('poll (explicit), timestamp {}'.format(timestamp))
        self.__do_poll(timestamp)

    def _startup(self):
        if self.__poll_interval == 0:
            logging.info('no automatic polling desired')
        else:
            logging.info('polling every {} seconds'.format(self.__poll_interval))
            self.__poll_timer_tag = GLib.timeout_add_seconds(self.__poll_interval, self.__poll_timer)

    def _shutdown(self):
        logging.info('stopping')
        if self.__poll_interval != 0:
            GLib.source_remove(self.__poll_timer_tag)

    def __poll_timer(self):
        now = timeutil.now_ts()
        logging.debug('poll (timer), timestamp {}'.format(now))
        self.__do_poll(timestamp=now)
        return True  # rearm timer

    def __do_poll(self, timestamp):
        for s in self.__services:
            s.poll(self.__bus, timestamp=timestamp)
