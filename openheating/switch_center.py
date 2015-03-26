from .switch import Switch
from .error import HeatingError

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
        self.get_switch(name).do_close()
    def do_open(self, name):
        self.get_switch(name).do_open()
    def is_closed(self, name):
        return self.get_switch(name).is_closed()
    def is_open(self, name):
        return self.get_switch(name).is_open()
   
    def get_switch(self, name):
        '''Returns an adapter onto self. The returned Switch delegates
        to self by name.
        '''
        return SwitchCenterSwitch(center=self, name=name)

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

