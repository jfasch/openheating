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


def read_thermometers(thing):
    context = {}
    exec(_make_code(thing), context)

    thermometers = context.get('THERMOMETERS')
    if thermometers is None:
        raise HeatingError('THERMOMETERS (iterable) expected but not there')
    _check_names(thermometers)
    return thermometers

def read_switches(thing):
    context = {}
    exec(_make_code(thing), context)
    
    switches = context.get('SWITCHES')
    if switches is None:
        raise HeatingError('SWITCHES (iterable) expected but not there')
    _check_names(switches)
    return switches

def read_circuits(thing):
    context = {}
    exec(_make_code(thing), context)
    
    circuits = context.get('CIRCUITS')
    if circuits is None:
        raise HeatingError('CIRCUITS (iterable) expected but not there')
    _check_names(circuits)
    return circuits

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
            
