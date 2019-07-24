from openheating.thermometer_fixed import FixedThermometer
from openheating.w1 import W1Thermometer
from openheating.error import HeatingError

from configparser import ConfigParser


class BadThermometerName(HeatingError):
    def __init__(self, msg):
        super().__init__(msg=msg, permanent=True)

def read_string(s):
    config = ConfigParser()
    config.read_string(s)
    return _parse(config)

def read_file(f):
    config = ConfigParser()
    if hasattr(f, 'read'):
        config.read_file(f)
    else:
        with open(f) as fh:
            config.read_file(fh)
    return _parse(config)

def _parse(config):
    thermometers = {}

    for name in config.sections():
        # the names are parts of DBus object names, so we restrict
        # them to, for example, not contain '-'. for the meantime,
        # str.isidentifier() looks like an easy thing to do.
        if not name.isidentifier():
            raise BadThermometerName('{} is not a valid DBus object path component'.format(name))

        type_ = config.get(name, 'Type')
        description = config.get(name, 'Description')

        if type_ == 'fixed':
            value = config.getfloat(name, 'Value')
            thermometers[name] = FixedThermometer(
                name=name, 
                description=description, 
                temperature=value)
        elif type_ == 'w1':
            path = config.get(name, 'Path')
            thermometers[name] = W1Thermometer(
                name=name,
                description=description,
                path=path)
        else:
            assert False

    return thermometers

