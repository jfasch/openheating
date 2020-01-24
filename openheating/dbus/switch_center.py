from . import interface_repo
from . import node
from . import error
from . import names
from . import _util
from .switch import Switch_Client


class SwitchCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = _util.get_iface(
            bus=bus,
            busname=names.Bus.SWITCHES,
            path='/',
            iface=interface_repo.SWITCHCENTER)

    @error.maperror
    def all_names(self):
        return self.__iface.all_names()

    @error.maperror
    def get_switch(self, name):
        return Switch_Client(proxy=_util.get_iface(
            bus=self.__bus,
            busname=names.Bus.SWITCHES,
            path='/switches/'+name, 
            iface=interface_repo.SWITCH))


@node.Definition(interfaces=interface_repo.get(interface_repo.SWITCHCENTER))
class SwitchCenter_Server:
    def __init__(self, objects):
        self.__objects = objects

    def all_names(self):
        return [o.get_name() for o in self.__objects]
