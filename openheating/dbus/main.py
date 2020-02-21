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
    def __init__(self, bus, servicedefs, interval):
        self.__bus = bus
        self.__servicedefs = servicedefs
        self.__poll_interval = int(interval)
        self.__poll_timer_tag = None   # valid after _startup()

    def poll(self, timestamp):
        logging.debug('poll (by D-Bus method call), timestamp {}'.format(timestamp))
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
        logging.debug('poll (by {}s timer), timestamp {}'.format(self.__poll_interval, now))
        self.__do_poll(timestamp=now)
        return True  # rearm timer

    def __do_poll(self, timestamp):
        for servicedef in self.__servicedefs:
            for path in servicedef.pollable_paths:
                client = Pollable_Client(bus=self.__bus, busname=servicedef.busname, path=path)
                client.poll(timestamp=timestamp)
