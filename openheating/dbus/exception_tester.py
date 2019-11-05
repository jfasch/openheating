from . import node
from . import names
from . import interface_repo
from ..base.error import HeatingError


class ExceptionTester_Client:
    def __init__(self, bus):
        self.__iface = bus.get(names.Bus.EXCEPTIONTESTER, '/')[names.Bus.EXCEPTIONTESTER]
    @node.maperror
    def raise_default_HeatingError(self, msg):
        return self.__iface.raise_default_HeatingError(msg)
    @node.maperror
    def raise_derived_default_HeatingError(self, msg):
        return self.__iface.raise_derived_default_HeatingError(msg)
    @node.maperror
    def raise_non_HeatingError(self):
        return self.__iface.raise_non_HeatingError()
        

@node.Definition(interfaces=interface_repo.get(interface_repo.EXCEPTIONTESTER))
class ExceptionTester_Server:
    class DerivedDefaultHeatingError(HeatingError):
        def __init__(self, message):
            super().__init__(message)
    def raise_default_HeatingError(self, msg):
        raise HeatingError(msg)
    def raise_derived_default_HeatingError(self, msg):
        raise self.DerivedDefaultHeatingError(msg)
    def raise_non_HeatingError(self):
        raise Exception()
