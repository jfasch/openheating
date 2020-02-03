from ..base.switch import FileSwitch

import os.path
import logging


class SwitchesConfig:
    def __init__(self, simulation_dir):
        self.__simulation_dir = simulation_dir
        self.__switches = [] # [(name, description, thermometer)]

    def get_switches(self):
        return self.__switches

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'ADD_SWITCH': self.__add_switch,
            'IS_SIMULATION': self.__simulation_dir is not None,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

    def __add_switch(self, name, description, fun, *args, **kwargs):
        if name in [name for name,_,_ in self.__switches]:
            raise DuplicateName(name)

        if self.__simulation_dir is None:
            sw = fun(*args, **kwargs)
        else:
            swfile = os.path.join(self.__simulation_dir, name)
            sw = FileSwitch(swfile, initial_value=False) # initial_value actually creates the file
            logging.info('simulation mode; {} is in file {}'.format(name, swfile))

        self.__switches.append((name, description, sw))
