#!/usr/bin/python3

from heating.thermometer_hwmon import HWMON_I2C_Thermometer

import sys

for spec_str in sys.argv[1:]:
    spec = spec_str.split(':')
    if len(spec) != 2:
        print('bad spec: '+spec_str, file=sys.stderr)
        sys.exit(1)
    print(HWMON_I2C_Thermometer(bus_number=int(spec[0]), address=int(spec[1], base=16)).temperature())

