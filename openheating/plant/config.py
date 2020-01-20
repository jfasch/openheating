from openheating.base.error import HeatingError


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
    def __init__(self):
        self.__simulated_thermometers_dir = None
        self.__update_interval = 5
        self.__thermometers = [] # [(name, description, thermometer)]

    def get_simulated_thermometers_dir(self):
        return self.__simulated_thermometers_dir
    def set_simulated_thermometers_dir(self, path):
        self.__simulated_thermometers_dir = path

    def get_update_interval(self):
        return self.__update_interval
    def set_update_interval(self, secs):
        self.__update_interval = secs

    def add_thermometer(self, name, description, th):
        if name in [name for name,_,_ in self.__thermometers]:
            raise DuplicateName(name)
        self.__thermometers.append((name, description, th))

    def get_thermometers(self):
        return self.__thermometers

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'GET_SIMULATED_THERMOMETERS_DIR': self.get_simulated_thermometers_dir,
            'GET_UPDATE_INTERVAL': self.get_update_interval,
            'SET_UPDATE_INTERVAL': self.set_update_interval,
            'ADD_THERMOMETER': self.add_thermometer,
            'GET_THERMOMETERS': self.get_thermometers,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

class SwitchesConfig:
    def __init__(self):
        self.__simulated_switches_dir = None
        self.__switches = []

    def get_simulated_switches_dir(self):
        return self.__simulated_switches_dir
    def set_simulated_switches_dir(self, path):
        self.__simulated_switches_dir = path
    
    def add_switch(self, sw):
        if sw.get_name() in [have.get_name() for have in self.__switches]:
            raise DuplicateName(sw.get_name())
        self.__switches.append(sw)
    def get_switches(self):
        return self.__switches

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'GET_SIMULATED_SWITCHES_DIR': self.get_simulated_switches_dir,
            'ADD_SWITCH': self.add_switch,
            'GET_SWITCHES': self.get_switches,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

class CircuitsConfig:
    def __init__(self):
        self.__circuits = []

    def add_circuit(self, c):
        if c.get_name() in [have.get_name() for have in self.__circuits]:
            raise DuplicateName(c.get_name())
        self.__circuits.append(c)
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
        self.__simulation_dir = None

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
            'GET_SIMULATION_DIR': self.get_simulation_dir,
            'ADD_SERVICE': self.add_service,
            'GET_SERVICES': self.get_services,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)
