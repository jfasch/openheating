from . import dbusutil
from ..error import HeatingError


class Errors_Client:
    def __init__(self, bus):
        self.__iface = bus.get(dbusutil.ERRORS_BUSNAME, '/')[dbusutil.ERRORS_IFACENAME]

    def num_errors(self):
        return self.__iface.num_errors()

class Errors_Server:
    def __init__(self):
        self.__num_errors = 0

    @dbusutil.unify_error
    def num_errors(self):
        return self.__num_errors

    def handle_error(self):
        pass

dbusutil.define_node(
    klass=Errors_Server,
    interfaces=(dbusutil.ERRORS_IFACEXML,)
)
