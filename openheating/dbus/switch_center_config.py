from .service_config import DBusServiceConfig
from .switch_client import DBusSwitch

from ..hardware.switch_gpio import GPIOSwitch
from ..hardware.gpio import create as gpio_create
from ..testutils.switch import TestSwitch

from abc import ABCMeta, abstractmethod


class SwitchCenterConfig(DBusServiceConfig):
    PATH = 'PATH'
    SWITCHES = 'SWITCHES'
    
    def __init__(self, content):
        DBusServiceConfig.__init__(
            self,
            symbols={
                'GPIOSwitch': _GPIOSwitchCreator,
                'TestSwitch': _TestSwitchCreator,
                'DBusSwitch': _DBusSwitchCreator,
                'OPEN': TestSwitch.OPEN,
                'CLOSED': TestSwitch.CLOSED,
                },
            content=content)

        self.__path = self.config()[self.PATH]
        self.__switches = self.config()[self.SWITCHES]

        assert type(self.__path) is str
        for name, creator in self.__switches:
            assert type(name) is str
            assert isinstance(creator, _Creator)

    def path(self):
        return self.__path
    def iter_switches(self):
        return self.__switches

class _Creator(metaclass=ABCMeta):
    @abstractmethod
    def create(self, connection_proxy):
        pass
    
class _GPIOSwitchCreator(_Creator):
    def __init__(self, number):
        self.__number = number
    def create(self, connection_proxy):
        return GPIOSwitch(gpio_create(self.__number))

class _TestSwitchCreator(_Creator):
    def __init__(self, initial_state):
        self.__initial_state = initial_state
    def create(self, connection_proxy):
        return TestSwitch(initial_state=self.__initial_state)

class _DBusSwitchCreator(_Creator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create(self, connection_proxy):
        return DBusSwitch(connection_proxy=connection_proxy, name=self.__name, path=self.__path)
