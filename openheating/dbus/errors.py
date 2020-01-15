from . import node
from . import error
from . import interface_repo
from . import names
from . import lifecycle

from ..base.error import HeatingError

import sys
import logging
import collections
import json


class Errors_Client:
    def __init__(self, bus):
        self.__iface = bus.get(names.Bus.ERRORS, '/')[interface_repo.ERRORS]
    @error.maperror
    def num_errors(self):
        return self.__iface.num_errors()
    @error.maperror
    def get_errors(self):
        return [node.DBusHeatingError.from_json(js) for js in self.__iface.get_errors()]


logger = logging.getLogger('dbus-errors')

@lifecycle.managed(startup='_start', shutdown='_stop')
@node.Definition(interfaces=interface_repo.get(interface_repo.ERRORS))
class Errors_Server:
    def __init__(self):
        self.__errors = collections.deque(maxlen=100)

    def num_errors(self):
        return len(self.__errors)

    def get_errors(self):
        return [str(e) for e in self.__errors]

    def handle_error(self, sender, object, iface, signal, *args):
        json_str = args[0][0] # wtf?
        try:
            e = node.DBusHeatingError.from_json(json_str)
            self.__errors.append(e)
        except json.JSONDecodeError as e:
            logger.exception('cannot parse error details')

    def _start(self):
        logger.info('starting')
    def _stop(self):
        logger.info('stopping')
