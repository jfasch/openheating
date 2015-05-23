from .switch import Switch
from ..base.error import HeatingError

from abc import ABCMeta, abstractmethod
import time


class SwitchCenterBase(metaclass=ABCMeta):
    @abstractmethod
    def all_names(self):
        return ['blah']

    @abstractmethod
    def set_state(self, name, value):
        pass

    @abstractmethod
    def get_state(self, name):
        pass

    def do_close(self, name):
        self.set_state(name, True)
    def do_open(self, name):
        self.set_state(name, False)
    def is_closed(self, name):
        return self.get_state(name) == True
    def is_open(self, name):
        return self.get_state(name) == False

class SwitchCenter(SwitchCenterBase):
    def __init__(self, switches):
        self.__switches = switches

    def all_names(self):
        return self.__switches.keys()

    def set_state(self, name, value):
        sw = self.__switches.get(name)
        if sw is None:
            raise HeatingError('no switch "%s"' % name)
        sw.set_state(value)

    def get_state(self, name):
        sw = self.__switches.get(name)
        if sw is None:
            raise HeatingError('no switch "%s"' % name)
        return sw.get_state()

    def num_switches__test(self):
        '''For tests only'''
        return len(self.__switches)
        
    def get_switch__test(self, name):
        '''For tests only'''
        return self.__switches.get(name)

class SwitchCenterSwitch(Switch):
    '''Is-a Switch which uses a SwitchCenter and a name to get to the real
    switch.
    '''
    def __init__(self, center, name):
        self.__center = center
        self.__name = name
    def set_state(self, value):
        self.__center.set_state(self.__name, value)
    def get_state(self):
        return self.__center.get_state(self.__name)

