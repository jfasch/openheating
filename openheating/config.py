from .thermometer_hwmon import HWMON_I2C_Thermometer
from .testutils.thermometer import TestThermometer

def parse_config(content):
    context = {
        'TestThermometer': TestThermometer,
        'HWMON_I2C_Thermometer': HWMON_I2C_Thermometer,
    }
    exec(content, context)
    
    return context

def parse_config_file(filename):
    return parse_config(open(filename).read())
