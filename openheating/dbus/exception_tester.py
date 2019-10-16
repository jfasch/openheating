from . import dbusutil
from ..error import HeatingError

from pydbus.error import error_registration


class ExceptionTester_Client:
    def __init__(self, bus):
        self.__iface = bus.get(dbusutil.EXCEPTIONTESTER_BUSNAME, '/')[dbusutil.EXCEPTIONTESTER_IFACENAME]
        

    def raise_base_HeatingError(self, msg):
        return self.__iface.raise_base_HeatingError(msg)

error_registration.map_error(HeatingError, dbusutil.HEATINGERROR_NAME)

class ExceptionTester_Server:
    def raise_base_HeatingError(self, msg):
        raise HeatingError(msg)

dbusutil.define_node(
    klass=ExceptionTester_Server,
    interfaces=(dbusutil.EXCEPTIONTESTER_IFACEXML,)
)

