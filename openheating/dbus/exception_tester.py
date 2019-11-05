from . import node
from . import names
from . import interface_repo
from ..base.error import HeatingError

import gi.repository

import json
import re


class ExceptionTester_Client:
    def __init__(self, bus):
        self.__iface = bus.get(names.Bus.EXCEPTIONTESTER, '/')[names.Bus.EXCEPTIONTESTER]
    def raise_default_HeatingError(self, msg):
        return self.__wrap(self.__iface.raise_default_HeatingError, msg)
    def raise_derived_default_HeatingError(self, msg):
        return self.__wrap(self.__iface.raise_derived_default_HeatingError, msg)
    def raise_non_HeatingError(self):
        return self.__wrap(self.__iface.raise_non_HeatingError)

    def __wrap(self, method, *args):
        try:
            return method(*args)
        except gi.repository.GLib.GError as e:
            pat = 'GDBus.Error:org.openheating.HeatingError: '
            assert e.message.find(pat) == 0
            js = e.message[len(pat):]
            raise HeatingError(details=json.loads(js))
        

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
