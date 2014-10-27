#!/usr/bin/env python

from heating import version

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
        'heating',
        ],

    scripts=[
        'bin/thermometer-dbus-service.py',
        ],

    data_files=[(os.path.join('share', name, 'debian'),
                 (
                     'debian/oh-functions',
                     'debian/oh-dbus-daemon',
                     'debian/oh-thermometer-dbus-service',
                     )),
    ]

    )
