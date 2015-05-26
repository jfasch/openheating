#!/usr/bin/env python

from openheating.base import version

import distutils.core
import os
import sys

PACKAGE_NAME = "openheating"

distutils.core.setup(
    name=PACKAGE_NAME,
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

    data_files=[
        # debian-style sysv init scripts
        ('/'.join(('share', PACKAGE_NAME, 'debian')),
         ('debian/openheating-lib.sh',
          'debian/openheating-dbus-daemon',
          'debian/openheating-dbus-services',
          'debian/openheating-sensors',)),

        # "faschingbauer" config files
        ('/'.join(('share', PACKAGE_NAME, 'installations/faschingbauer/config/heizraum/etc/openheating')),
         ('installations/faschingbauer/config/heizraum/etc/openheating/openheating-dbus-daemon.conf',
          'installations/faschingbauer/config/heizraum/etc/openheating/openheating-dbus-services.conf',
          'installations/faschingbauer/config/heizraum/etc/openheating/openheating-sensors.conf',)),
        ('/'.join(('share', PACKAGE_NAME, 'installations/faschingbauer/config/waschraum/etc/openheating')),
         ('installations/faschingbauer/config/waschraum/etc/openheating/openheating-dbus-services.conf',
          'installations/faschingbauer/config/waschraum/etc/openheating/openheating-sensors.conf',)),
        ('/'.join(('share', PACKAGE_NAME, 'installations/faschingbauer/config/ofen/etc/openheating')),
         ('installations/faschingbauer/config/ofen/etc/openheating/openheating-dbus-services.conf',
          'installations/faschingbauer/config/ofen/etc/openheating/openheating-sensors.conf',)),
        ('/'.join(('share', PACKAGE_NAME, 'installations/faschingbauer/config/essraum/etc/openheating')),
         ('installations/faschingbauer/config/essraum/etc/openheating/openheating-dbus-services.conf',
          'installations/faschingbauer/config/essraum/etc/openheating/openheating-sensors.conf',)),
        ('/'.join(('share', PACKAGE_NAME, 'installations/faschingbauer/config/switch-test/etc/openheating')),
         ('installations/faschingbauer/config/switch-test/etc/openheating/openheating-dbus-services.conf',)),

        # "glt2015" config files
        ('/'.join(('share', PACKAGE_NAME, 'installations/glt2015/brett/etc/openheating')),
         ('installations/glt2015/brett/etc/openheating/openheating-dbus-services.conf',
          'installations/glt2015/brett/etc/openheating/openheating-dbus-daemon.conf',)),
        ('/'.join(('share', PACKAGE_NAME, 'installations/glt2015/laptop/etc/openheating')),
         ('installations/glt2015/brett/etc/openheating/openheating-dbus-services.conf',)),
    ],
)
