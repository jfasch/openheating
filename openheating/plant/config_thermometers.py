from ..base.thermometer import FileThermometer

import os.path
import logging


class ThermometersConfig:
    def __init__(self, simulation_dir):
        self.__simulation_dir = simulation_dir
        self.__thermometers = [] # [(name, description, thermometer)]

    def get_thermometers(self):
        return self.__thermometers

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'ADD_THERMOMETER': self.__add_thermometer,
            'IS_SIMULATION': self.__simulation_dir is not None,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

    def __add_thermometer(self, name, description, cls, *args, **kwargs):
        if name in [name for name,_,_ in self.__thermometers]:
            raise DuplicateName(name)

        if self.__simulation_dir is None:
            th = cls(*args, **kwargs)
        else:
            # ignore thermometer, and create a simulated one.
            thfile = os.path.join(self.__simulation_dir, name)
            th = FileThermometer(thfile, initial_value=20) # initial_value actually creates the file
            logging.info('simulation mode; {} is in file {}'.format(name, thfile))

        self.__thermometers.append((name, description, th))

