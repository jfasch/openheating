from openheating.base.thermometer import FixedThermometer, ErrorThermometer
from openheating.base.w1 import W1Thermometer
from openheating.base.error import HeatingError, BadDBusPathComponent

from configparser import ConfigParser


class DuplicateError(HeatingError):
    def __init__(self, name):
        super().__init__(msg='Duplicate thermometer {}'.format(name))

def read_ini(conf):
    config = ConfigParser()

    if hasattr(conf, 'read'):
        config.read_file(conf)
    elif type(conf) is str:
        config.read_string(conf)
    else:
        config.read_string('\n'.join(conf))

    return _parse_ini(config)

def read_pyconf(conf):
    if hasattr(conf, 'read'):
        code = conf.read()
    elif type(conf) is str:
        code = conf
    else:
        code = '\n'.join(conf)

    thermometers = {}
    context = {'THERMOMETERS': thermometers}
    exec(code, context)
    for name in thermometers.keys():
        if not name.isidentifier():
            raise BadDBusPathComponent(name=name)
    return thermometers

def _parse_ini(config):
    thermometers = {}

    for name in config.sections():
        # the names are parts of DBus object names, so we restrict
        # them to, for example, not contain '-'. for the meantime,
        # str.isidentifier() looks like an easy thing to do.
        if not name.isidentifier():
            raise BadDBusPathComponent(name=name)

        type_ = config.get(name, 'Type')
        description = config.get(name, 'Description')

        if type_ == 'fixed':
            value = config.getfloat(name, 'Value')
            thermometers[name] = FixedThermometer(
                name=name, 
                description=description, 
                temperature=value)
        elif type_ == 'error':
            n_ok_before_error = config.getint(name, 'NOkBeforeError')
            thermometers[name] = ErrorThermometer(
                name=name, 
                description=description,
                n_ok_before_error = n_ok_before_error)
        elif type_ == 'w1':
            path = config.get(name, 'Path')
            thermometers[name] = W1Thermometer(
                name=name,
                description=description,
                path=path)
        else:
            assert False

    return thermometers
