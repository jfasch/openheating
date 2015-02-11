#!/usr/bin/python3

from openheating.hardware.thermometer_hwmon import HWMON_I2C_Thermometer

import sys

for spec_str in sys.argv[1:]:
    spec = spec_str.split(':')
    if len(spec) != 3:
        print('bad spec: '+spec_str, file=sys.stderr)
        sys.exit(1)
    bus = int(spec[0])
    address = int(spec[1], base=16)
    driver = spec[2]
    print(HWMON_I2C_Thermometer(bus_number=bus, address=address, driver=driver).temperature())

