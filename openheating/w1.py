from .thermometer import Thermometer
from .error import HeatingError

import re
import os
import os.path


_w1dir = '/sys/bus/w1/devices'
_re_devdir = re.compile(r'^(\d+)-([0-9a-z]+)$')
_re_crc = re.compile(r'^.*: crc=\S+\s+(\S*)$')
_re_temp = re.compile(r'^.* t=(\d+)$')

def available_thermometers():
    for entry in os.listdir(_w1dir):
        try:
            yield W1Thermometer(
                name='dummy-name',
                description='dummy-description', 
                path=os.path.join(_w1dir, entry))
        except W1Thermometer.BadPath:
            continue

class W1Thermometer(Thermometer):
    class BadPath(HeatingError):
        def __init__(self, msg):
            super().__init__(msg)

    def __init__(self, name, description, path):
        hit = _re_devdir.search(os.path.basename(path))
        if hit is None:
            raise self.BadPath('{} does not look like a w1 device'.format(path))

        super().__init__()

        self.name = name
        self.description = description
        self.path = path
        self.type = hit.group(1)
        self.id = hit.group(2)

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_temperature(self):
        with open(os.path.join(self.path, 'w1_slave')) as w1_slave:
            lines = w1_slave.readlines()

        temperature = None
        for line in lines:
            crc_match = _re_crc.search(line)
            if crc_match:
                  if crc_match.group(1) != 'YES':
                      raise HeatingError('CRC error in {}'.format(self.path))

            temp_match = _re_temp.search(line)
            if temp_match:
                temperature = float(temp_match.group(1))/1000
        
        assert temperature is not None
        return temperature
