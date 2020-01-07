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


def read(thing, bus, name, context):
    the_context = { 'BUS': bus }
    the_context.update(context)
    exec(_make_code(thing), the_context)

    objs = the_context.get(name)
    if objs is None:
        raise HeatingError('{} (iterable) expected but not there'.format(name))
    _check_names(objs)
    return objs

def read_thermometers(thing, bus, simulated_thermometers_dir):
    return read(thing, bus, 'THERMOMETERS', {'SIMULATED_THERMOMETERS_DIR': simulated_thermometers_dir})

def read_switches(thing, bus):
    return read(thing, bus, 'SWITCHES')

def read_circuits(thing, bus):
    return read(thing, bus, 'CIRCUITS')

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
            
