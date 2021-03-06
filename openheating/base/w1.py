from .thermometer import Thermometer
from .error import HeatingError

import re
import os
import os.path
import logging


_w1dir = '/sys/bus/w1/devices'
_re_devdir = re.compile(r'^(\d+)-([0-9a-z]+)$')
_re_crc = re.compile(r'^.*: crc=\S+\s+(\S*)$')
_re_temp = re.compile(r'^.* t=(\d+)$')

def available_thermometers():
    for entry in os.listdir(_w1dir):
        try:
            yield W1Thermometer(path=os.path.join(_w1dir, entry))
        except W1Thermometer.BadPath:
            continue

class W1ReadError(HeatingError):
    def __init__(self, filename):
        super().__init__(details={
            'category': 'w1',
            'message': 'cannot read file {}'.format(filename),
            'w1': {
                'issue': 'file read error',
                'file': filename,
            },
        })

class W1Thermometer(Thermometer):
    class BadPath(HeatingError):
        def __init__(self, msg):
            super().__init__(msg)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.type, self.id = self.__type_id_from_path(path)

    def get_temperature(self):
        filename = os.path.join(self.path, 'w1_slave')
        try:
            with open(filename) as w1_slave:
                lines = w1_slave.readlines()
        except (FileNotFoundError, IOError):
            raise W1ReadError(filename=filename)

        temperature = None
        for line in lines:
            crc_match = _re_crc.search(line)
            if crc_match:
                  if crc_match.group(1) != 'YES':
                      logging.exception('CRC error reading file {}'.format(filename))
                      raise W1ReadError(filename=filename)

            temp_match = _re_temp.search(line)
            if temp_match:
                temperature = float(temp_match.group(1))/1000
        
        assert temperature is not None
        return temperature

    @classmethod
    def id_from_path(cls, path):
        type, id = cls.__type_id_from_path(path)
        return id

    @classmethod
    def __type_id_from_path(cls, path):
        hit = _re_devdir.search(os.path.basename(path))
        if hit is None:
            raise cls.BadPath('{} does not look like a w1 device'.format(path))
        return hit.group(1), hit.group(2)
        
        
