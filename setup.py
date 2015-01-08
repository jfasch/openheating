#!/usr/bin/env python

from openheating import version

import distutils.core
import os
import sys

name = "openheating"

distutils.core.setup(
    name=name,
    version=version.VERSION,
    description="openheating",
    author="Joerg Faschingbauer",
    author_email="jf@faschingbauer.co.at",
    url='http://dev.null.org',

    packages=[
        'openheating',
        'openheating.dbus',
        'openheating.hardware',
        'openheating.testutils',
        ],

    scripts=[
        'bin/openheating-dbus-thermometer-service.py',
        'bin/openheating-dbus-thermometer-center.py',
        'bin/openheating-dbus-switch-service.py',
        'bin/openheating-dbus-switch-center.py',
        'bin/openheating-sensors.py',
        ],

    data_files=[(os.path.join('share', name, 'debian'),
                 ('debian/openheating-lib.sh',
                  'debian/openheating-dbus-daemon',
                  'debian/openheating-dbus-thermometer-service',
                  'debian/openheating-dbus-thermometer-center',
                  'debian/openheating-dbus-switch-service',
                  'debian/openheating-dbus-switch-center',
                  'debian/openheating-sensors',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/heizraum/etc/openheating'),
                 ('config/faschingbauer/heizraum/etc/openheating/openheating-dbus-daemon.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-dbus-thermometer-service.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-dbus-thermometer-center.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-dbus-switch-center.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/boiler/etc/openheating'),
                 ('config/faschingbauer/boiler/etc/openheating/openheating-dbus-thermometer-service.conf',
                  'config/faschingbauer/boiler/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/ofen/etc/openheating'),
                 ('config/faschingbauer/ofen/etc/openheating/openheating-dbus-thermometer-service.conf',
                  'config/faschingbauer/ofen/etc/openheating/openheating-dbus-switch-service.conf',
                  'config/faschingbauer/ofen/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/switch-test/etc/openheating'),
                 ('config/faschingbauer/switch-test/etc/openheating/openheating-dbus-switch-service.conf',
                  )),
                ]
    )
