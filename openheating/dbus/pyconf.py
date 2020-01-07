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
        self.__thermometers = []

    def get_simulated_thermometers_dir(self):
        return self.__simulated_thermometers_dir
    def set_simulated_thermometers_dir(self, path):
        self.__simulated_thermometers_dir = path

    def get_update_interval(self):
        return self.__update_interval
    def set_update_interval(self, secs):
        self.__update_interval = secs

    def add_thermometer(self, th):
        if th.get_name() in [have.get_name() for have in self.__thermometers]:
            raise DuplicateName(th.get_name())
        self.__thermometers.append(th)

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

def read(thing, bus, name, context):
    the_context = { 'BUS': bus }
    the_context.update(context)
    exec(_make_code(thing), the_context)

    objs = the_context.get(name)
    if objs is None:
        raise HeatingError('{} (iterable) expected but not there'.format(name))
    _check_names(objs)
    return objs

def read_switches(thing, bus):
    return read(thing, bus, 'SWITCHES', {})

def read_circuits(thing, bus):
    return read(thing, bus, 'CIRCUITS', {})

def _make_code(thing):
    if hasattr(thing, 'read'):
        code = thing.read()
    elif type(thing) is str:
        code = thing
    else:
        code = '\n'.join(thing)
    return code

def _check_names(sequence):
    names = set()
    for item in sequence:
        name = item.get_name()
        if name in names:
            raise DuplicateName(name)
        if not name.isidentifier():
            raise BadName(name)
        names.add(name)
            
