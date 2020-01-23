from openheating.base.error import HeatingError
from openheating.base.thermometer import FileThermometer
from openheating.base.switch import FileSwitch

import logging
import os.path


class DuplicateName(HeatingError):
    def __init__(self, name):
        super().__init__(msg='duplicate name detected: "{}"'.format(name))
        self.name = name

class BadName(HeatingError):
    """Used where e.g. a thermometer configuration gives the thermometer
    a name that is unusable in a DBus object path"""
    def __init__(self, name):
        super().__init__(msg='{} is not a valid name (has to be a Python identifier'.format(name))
        self.name = name

class ThermometersConfig:
    def __init__(self, simulation_dir):
        self.__simulation_dir = simulation_dir
        self.__update_interval = 5
        self.__thermometers = [] # [(name, description, thermometer)]

    def get_update_interval(self):
        return self.__update_interval

    def set_update_interval(self, secs):
        self.__update_interval = secs

    def get_thermometers(self):
        return self.__thermometers

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'SET_UPDATE_INTERVAL': self.set_update_interval,
            'ADD_THERMOMETER': self.__add_thermometer,
            'IS_SIMULATION': self.__simulation_dir is not None,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

    def __add_thermometer(self, name, description, th=None):
        if name in [name for name,_,_ in self.__thermometers]:
            raise DuplicateName(name)

        if self.__simulation_dir is None:
            if th is None:
                raise HeatingError('cannot ADD_THERMOMETER "{}" as None when not simulating'.format(name))
        else:
            if th is not None:
                raise HeatingError('cannot ADD_THERMOMETER "{}" as not None when simulating'.format(name))
            thfile = os.path.join(self.__simulation_dir, name)
            th = FileThermometer(thfile, initial_value=20) # initial_value actually creates the file
            logging.info('simulation mode; {} is in file {}'.format(name, thfile))

        self.__thermometers.append((name, description, th))

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

    def __add_switch(self, name, description, sw=None):
        if name in [name for name,_,_ in self.__switches]:
            raise DuplicateName(name)

        if self.__simulation_dir is None:
            if sw is None:
                raise HeatingError('cannot ADD_SWITCH "{}" as None when not simulating'.format(name))
        else:
            if sw is not None:
                raise HeatingError('cannot ADD_SWITCH "{}" as not None when simulating'.format(name))
            swfile = os.path.join(self.__simulation_dir, name)
            sw = FileSwitch(swfile, initial_value=False) # initial_value actually creates the file
            logging.info('simulation mode; {} is in file {}'.format(name, swfile))

        self.__switches.append((name, description, sw))

class CircuitsConfig:
    def __init__(self):
        self.__circuits = [] # [(name, description, thermometer)]

    def add_circuit(self, name, description, c):
        if name in [name for name,_,_ in self.__circuits]:
            raise DuplicateName(name)
        self.__circuits.append((name, description, c))
    def get_circuits(self):
        return self.__circuits

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'ADD_CIRCUIT': self.add_circuit,
            'GET_CIRCUITS': self.get_circuits,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

class RunnerConfig:
    def __init__(self):
        self.__services = []
        self.__interval = 4
        self.__simulation_dir = None

    def get_interval(self):
        return self.__interval
    def set_interval(self, secs):
        self.__interval = secs

    def get_simulation_dir(self):
        return self.__simulation_dir
    def set_simulation_dir(self, path):
        self.__simulation_dir = path

    def add_service(self, s):
        self.__services.append(s)
    def get_services(self):
        return self.__services

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'SET_INTERVAL': self.set_interval,
            'IS_SIMULATION': self.__simulation_dir is not None,
            'GET_SIMULATION_DIR': self.get_simulation_dir,
            'ADD_SERVICE': self.add_service,
            'GET_SERVICES': self.get_services,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)
