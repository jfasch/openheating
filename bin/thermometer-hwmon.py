#!/usr/bin/python3

import heating.thermometer_hwmon as thermometer_hwmon

for number, th in thermometer_hwmon.iter_devices():
    print(th.temperature())
