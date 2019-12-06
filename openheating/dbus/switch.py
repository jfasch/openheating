from . import node
from . import interface_repo

from ..base.switch import Switch


class Switch_Client(Switch):
    def __init__(self, proxy):
        super().__init__()
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
    def set_state(self, state):
        self.__proxy.set_state(state)

    @node.maperror
    def get_state(self):
        return self.__proxy.get_state()

@node.Definition(interfaces=interface_repo.get(interface_repo.SWITCH))
class Switch_Server:
    def __init__(self, switch):
        self.__switch = switch

    def get_name(self):
        return self.__switch.get_name()

    def get_description(self):
        return self.__switch.get_description()

    def set_state(self, state):
        self.__switch.set_state(state)
        
    def get_state(self):
        return self.__switch.get_state()