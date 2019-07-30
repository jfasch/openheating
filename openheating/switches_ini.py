from .switch import DummySwitch
from . import gpio
from openheating.error import BadDBusPathComponent

from configparser import ConfigParser


def read_string(s, dummy=False):
    config = ConfigParser()
    config.read_string(s)
    return _parse(config, dummy)

def read_file(f, dummy=False):
    config = ConfigParser()
    if hasattr(f, 'read'):
        config.read_file(f)
    else:
        with open(f) as fh:
            config.read_file(fh)
    return _parse(config, dummy)

def _parse(config, dummy):
    switches = {}

    for name in config.sections():
        # the names are parts of DBus object names, so we restrict
        # them to, for example, not contain '-'. for the meantime,
        # str.isidentifier() looks like an easy thing to do.
        if not name.isidentifier():
            raise BadDBusPathComponent(name=name)

        type_ = config.get(name, 'Type')
        description = config.get(name, 'Description')

        if type_ == 'dummy':
            state = config.getboolean(name, 'State')
            switches[name] = DummySwitch(
                name=name, 
                description=description, 
                state=state)
        elif type_ == 'gpio':
            chiplabel = config.get(name, 'ChipLabel')
            offset = config.get(name, 'Offset')
            direction = config.get(name, 'Direction')

            if chiplabel is None:
                raise HeatingError('{}: ChipLabel is missing'.format(name))
            if offset is None:
                raise HeatingError('{}: Offset is missing'.format(name))
            if direction is None:
                raise HeatingError('{}: Direction is missing'.format(name))
            if direction.lower() == 'in':
                direction = gpio.DIRECTION_IN
            elif direction.lower() == 'out':
                direction = gpio.DIRECTION_OUT
            else:
                raise HeatingError('{}: bad "Direction" value: {}'.format(name, direction))
                
            switches[name] = gpio.create_switch(name=name, 
                                                description=description, 
                                                chiplabel=chiplabel, 
                                                offset=offset, 
                                                direction=direction, 
                                                dummy=dummy)
        else:
            raise HeatingError('Bad switch type')

    return switches
