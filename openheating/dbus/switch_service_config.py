from .service_config import DBusServiceConfig

from ..hardware.switch_gpio import GPIOSwitch
from ..hardware import gpio
from ..testutils.switch import TestSwitch

import os.path

class SwitchServiceConfig(DBusServiceConfig):
    PARENT_PATH = 'PARENT_PATH'
    SWITCHES = 'SWITCHES'
    
    def __init__(self, content):
        DBusServiceConfig.__init__(
            self,
            symbols={
                'GPIOSwitch': _GPIOSwitch,
                'TestSwitch': TestSwitch,
                'OPEN': TestSwitch.OPEN,
                'CLOSED': TestSwitch.CLOSED,
                },
            content=content)

        self.__parent_path = self.config().get('PARENT_PATH')
        switches = self.config().get('SWITCHES')

        if self.__parent_path is None:
            raise HeatingError('"PARENT_PATH" not specified')
        if switches is None:
            raise HeatingError('"SWITCHES" not specified')

        self.__switches = []
        for s in switches:
            self.__switches.append({'object_path': os.path.join(self.__parent_path, s[0]),
                                    'switch': s[1]})

    def switches(self):
        return self.__switches

class _GPIOSwitch(GPIOSwitch):
    # create switch by gpio number rather than by gpio object. in the
    # config file we don't want to bother the user with our internals.
    def __init__(self, number):
        GPIOSwitch.__init__(self, gpio.create(number))
