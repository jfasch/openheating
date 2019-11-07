from openheating.base.thermometer import FixedThermometer, ErrorThermometer
from openheating.base.w1 import W1Thermometer
from openheating.base.error import HeatingError, BadDBusPathComponent

from configparser import ConfigParser


def read(conf):
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
