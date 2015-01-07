from .switch import Switch
from .error import HeatingError

from abc import ABCMeta, abstractmethod
import time

class SwitchCenterBase(metaclass=ABCMeta):
    OPEN, CLOSED = Switch.states

    @abstractmethod
    def all_names(self):
        return ['blah']

    @abstractmethod
    def set_state(self, name, state):
        pass

    @abstractmethod
    def get_state(self, name):
        pass

    def do_close(self, name):
        self.get_switch(name).set_state(self.CLOSED)
    def do_open(self, name):
        self.get_switch(name).set_state(self.OPEN)
    def is_closed(self, name):
        return self.get_switch(name).get_state() == self.CLOSED
    def is_open(self, name):
        return self.get_switch(name).get_state() == self.OPEN
   
    def get_switch(self, name):
        '''Returns an adapter onto self. The returned Switch delegates
        to self by name.
        '''
        return self._Adapter(center=self, name=name)

    class _Adapter(Switch):
        def __init__(self, center, name):
            self.__center = center
            self.__name = name
        def set_state(self, state):
            self.__center.set_state(self.__name, state)
        def get_state(self):
            self.__center.get_state(self.__name)


class SwitchCenter(SwitchCenterBase):
    def __init__(self, switches):
        self.__switches = {}
        for name, sw in switches:
            if name in self.__switches:
                raise HeatingError('duplicate switch "%s"' % name)
            self.__switches[name] = sw

    def all_names(self):
        return self.__switches.keys()

    def set_state(self, name, state):
        sw = self.__switches.get(name)
        if sw is None:
            raise HeatingError('no switch "%s"' % name)
        sw.set_state(state)

    def get_state(self, name):
        sw = self.__switches.get(name)
        if sw is None:
            raise HeatingError('no switch "%s"' % name)
        return sw.get_state()
