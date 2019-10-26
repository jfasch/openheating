from . import dbusutil
from .util import lifecycle
from ..error import HeatingError

import sys
import logging
import collections
import json


class Errors_Client:
    def __init__(self, bus):
        self.__iface = bus.get(dbusutil.ERRORS_BUSNAME, '/')[dbusutil.ERRORS_IFACENAME]

    def num_errors(self):
        return self.__iface.num_errors()


logger = logging.getLogger('dbus-errors')

@lifecycle.managed(startup='_start', shutdown='_stop')
class Errors_Server:
    def __init__(self):
        self.__errors = collections.deque(maxlen=100)

    @dbusutil.unify_error
    def num_errors(self):
        return len(self.__errors)

    def handle_error(self, sender, object, iface, signal, *args):
        json_str = args[0][0] # wtf?
        try:
            details = json.loads(json_str)
            self.__errors.append(HeatingError(details=details))
        except json.JSONDecodeError as e:
            logger.exception('cannot parse error details')

    def _start(self):
        logger.info('starting')
    def _stop(self):
        logger.info('stopping')

dbusutil.define_node(
    klass=Errors_Server,
    interfaces=(dbusutil.ERRORS_IFACEXML,)
)
