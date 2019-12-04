from . import node
from . import interface_repo

from ..base.circuit import Circuit


class Circuit_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

        # cached attributes
        self.__name = self.__description = None
        
    @node.maperror
    def get_name(self):
        if self.__name is None:
            self.__name = self.__proxy.get_name()
        return self.__name
        
    @node.maperror
    def get_description(self):
        if self.__description is None:
            self.__description = self.__proxy.get_description()
        return self.__description

    @node.maperror
    def activate(self):
        self.__proxy.activate()

    @node.maperror
    def deactivate(self):
        return self.__proxy.deactivate()

    @node.maperror
    def is_active(self):
        return self.__proxy.is_active()

    @node.maperror
    def poll(self, timestamp):
        return self.__proxy.poll()

@node.Definition(interfaces=interface_repo.get(interface_repo.CIRCUIT))
class Circuit_Server:
    def __init__(self, circuit):
        self.__circuit = circuit

    def get_name(self):
        return self.__circuit.get_name()

    def get_description(self):
        return self.__circuit.get_description()

    def activate(self):
        return self.__circuit.activate()

    def deactivate(self):
        return self.__circuit.deactivate()

    def is_active(self):
        return self.__circuit.is_active()

    def poll(self, timestamp):
        return self.__circuit.poll(timestamp)
