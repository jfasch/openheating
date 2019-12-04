from . import interface_repo
from . import node
from . import names
from .circuit import Circuit_Client


class CircuitCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=names.Bus.CIRCUITS,
            path='/',
            iface=interface_repo.CIRCUITCENTER)

    @node.maperror
    def all_names(self):
        return self.__iface.all_names()

    @node.maperror
    def get_circuit(self, name):
        return Circuit_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.CIRCUITS,
                path='/circuits/'+name, 
                iface=interface_repo.CIRCUIT))

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]


@node.Definition(interfaces=interface_repo.get(interface_repo.CIRCUITCENTER))
class CircuitCenter_Server:
    def __init__(self, circuits):
        self.__circuits = circuits

    def all_names(self):
        return [c.get_name() for c in self.__circuits]
