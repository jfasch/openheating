from . import interface_repo
from . import node
from . import error
from . import names
from .switch import Switch_Client


class SwitchCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=names.Bus.SWITCHES,
            path='/',
            iface=interface_repo.SWITCHCENTER)

    @error.maperror
    def all_names(self):
        return self.__iface.all_names()

    @error.maperror
    def get_switch(self, name):
        return Switch_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.SWITCHES,
                path='/switches/'+name, 
                iface=interface_repo.SWITCH))

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]


@node.Definition(interfaces=interface_repo.get(interface_repo.SWITCHCENTER))
class SwitchCenter_Server:
    def __init__(self, names):
        self.__names = names

    def all_names(self):
        return self.__names
