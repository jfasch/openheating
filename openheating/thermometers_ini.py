from openheating.thermometer_fixed import FixedThermometer

from configparser import ConfigParser


def read(f):
    thermometers = {}
    config = ConfigParser()
    config.read_file(f)
    for thermometer_name in config.sections():
        type_ = config.get(thermometer_name, 'Type')
        value = config.getfloat(thermometer_name, 'Value')

        if type_ == 'fixed':
            thermometers[thermometer_name] = FixedThermometer(value)
        else:
            assert False

    return thermometers

    
