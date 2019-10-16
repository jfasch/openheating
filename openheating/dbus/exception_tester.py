from . import dbusutil
from ..error import HeatingError

class ExceptionTester_Client:
    def __init__(self, bus):
        self.__iface = bus.get(dbusutil.EXCEPTIONTESTER_BUSNAME, '/')[dbusutil.EXCEPTIONTESTER_IFACENAME]
    def raise_default_HeatingError(self, msg):
        return self.__iface.raise_default_HeatingError(msg)
    def raise_derived_default_HeatingError(self, msg):
        return self.__iface.raise_derived_default_HeatingError(msg)

class ExceptionTester_Server:
    class DerivedDefaultHeatingError(HeatingError):
        def __init__(self, message):
            super().__init__(message)
    @dbusutil.unify_error
    def raise_default_HeatingError(self, msg):
        raise HeatingError(msg)
    @dbusutil.unify_error
    def raise_derived_default_HeatingError(self, msg):
        raise self.DerivedDefaultHeatingError(msg)

dbusutil.define_node(
    klass=ExceptionTester_Server,
    interfaces=(dbusutil.EXCEPTIONTESTER_IFACEXML,)
)

