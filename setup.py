#!/usr/bin/env python

from openheating.base import version

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
        'openheating.base',
        'openheating.logic',
        'openheating.dbus',
        'openheating.hardware',
        'openheating.testutils',
        ],

    scripts=[
        'bin/openheating-dbus-services.py',
        'bin/openheating-sensors.py',
        ],

    data_files=[('/'.join(('share', name, 'debian')),
                 ('debian/openheating-lib.sh',
                  'debian/openheating-dbus-daemon',
                  'debian/openheating-dbus-services',
                  'debian/openheating-sensors',
                  )),
                ('/'.join(('share', name, 'installations/faschingbauer/config/heizraum/etc/openheating')),
                 ('installations/faschingbauer/config/heizraum/etc/openheating/openheating-dbus-daemon.conf',
                  'installations/faschingbauer/config/heizraum/etc/openheating/openheating-dbus-services.conf',
                  'installations/faschingbauer/config/heizraum/etc/openheating/openheating-sensors.conf',
                  )),
                ('/'.join(('share', name, 'installations/faschingbauer/config/waschraum/etc/openheating')),
                 ('installations/faschingbauer/config/waschraum/etc/openheating/openheating-dbus-services.conf',
                  'installations/faschingbauer/config/waschraum/etc/openheating/openheating-sensors.conf',
                  )),
                ('/'.join(('share', name, 'installations/faschingbauer/config/ofen/etc/openheating')),
                 ('installations/faschingbauer/config/ofen/etc/openheating/openheating-dbus-services.conf',
                  'installations/faschingbauer/config/ofen/etc/openheating/openheating-sensors.conf',
                  )),
                ('/'.join(('share', name, 'installations/faschingbauer/config/essraum/etc/openheating')),
                 ('installations/faschingbauer/config/essraum/etc/openheating/openheating-dbus-services.conf',
                  'installations/faschingbauer/config/essraum/etc/openheating/openheating-sensors.conf',
                  )),
                ('/'.join(('share', name, 'installations/faschingbauer/config/switch-test/etc/openheating')),
                 ('installations/faschingbauer/config/switch-test/etc/openheating/openheating-dbus-services.conf',
                  )),
                ]
    )
