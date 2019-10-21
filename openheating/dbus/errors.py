from . import dbusutil
from .util import lifecycle
from ..error import HeatingError

import sys
import logging


class Errors_Client:
    def __init__(self, bus):
        self.__iface = bus.get(dbusutil.ERRORS_BUSNAME, '/')[dbusutil.ERRORS_IFACENAME]

    def num_errors(self):
        return self.__iface.num_errors()


logger = logging.getLogger('dbus-errors')

@lifecycle.managed(startup='_start', shutdown='_stop')
class Errors_Server:
    def __init__(self):
        self.__num_errors = 0

    @dbusutil.unify_error
    def num_errors(self):
        return self.__num_errors

    def handle_error(self, sender, object, iface, signal, json):
        print('jjjj handle_error sender {}, object {}, iface {}, signal {}, json {}'.format(sender, object, iface, signal, json), file=sys.stderr)
        self.__num_errors += 1

    def _start(self):
        logger.info('starting')
    def _stop(self):
        logger.info('stopping')

dbusutil.define_node(
    klass=Errors_Server,
    interfaces=(dbusutil.ERRORS_IFACEXML,)
)
