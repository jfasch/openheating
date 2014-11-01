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
        ],

    scripts=[
        'bin/openheating-dbus-thermometer-service.py',
        ],

    data_files=[(os.path.join('share', name, 'debian'),
                 (
                     'debian/openheating-lib.sh',
                     'debian/openheating-dbus-daemon',
                     'debian/openheating-dbus-thermometer-service',
                     )),
                (os.path.join('share', name, 'config'),
                 (
                     'config/openheating-dbus-daemon.conf',
                     'config/openheating-dbus-thermometer-service.conf',
                     )),
    ]

    )
