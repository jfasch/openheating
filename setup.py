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
        'bin/openheating-dbus-services.py',
        'bin/openheating-sensors.py',
        ],

    data_files=[(os.path.join('share', name, 'debian'),
                 ('debian/openheating-lib.sh',
                  'debian/openheating-dbus-daemon',
                  'debian/openheating-dbus-services',
                  'debian/openheating-sensors',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/heizraum/etc/openheating'),
                 ('config/faschingbauer/heizraum/etc/openheating/openheating-dbus-daemon.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-dbus-services.conf',
                  'config/faschingbauer/heizraum/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/waschraum/etc/openheating'),
                 ('config/faschingbauer/waschraum/etc/openheating/openheating-dbus-services.conf',
                  'config/faschingbauer/waschraum/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/ofen/etc/openheating'),
                 ('config/faschingbauer/ofen/etc/openheating/openheating-dbus-services.conf',
                  'config/faschingbauer/ofen/etc/openheating/openheating-sensors.conf',
                  )),
                (os.path.join('share', name, 'config/faschingbauer/switch-test/etc/openheating'),
                 ('config/faschingbauer/switch-test/etc/openheating/openheating-dbus-services.conf',
                  )),
                ]
    )
