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

class PlantConfig:
    def __init__(self):
        self.__services = []
        self.__simulation_dir = None

    def get_simulation_dir(self):
        return self.__simulation_dir
    def set_simulation_dir(self, path):
        self.__simulation_dir = path

    def add_service(self, service):
        if service.busname in [s.busname for s in self.__services]:
            raise DuplicateName(service.busname)
        self.__services.append(service)
    def get_services(self):
        return self.__services

    def parse(self, path):
        context = {
            'IS_SIMULATION': self.__simulation_dir is not None,
            'GET_SIMULATION_DIR': self.get_simulation_dir,
            'ADD_SERVICE': self.add_service,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)
