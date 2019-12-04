#!/usr/bin/python3

from distutils.core import setup
from distutils.command.install_data import install_data

import os
import string

# PROBLEM: install systemd unit files. these usually refer to
# executables to be started. we do not want to hardcode the paths
# (say, always install to prefix=/usr), but rather substitute the
# install-time provided --prefix=...

# SOLUTION: 

# do it almost like autoconf's AC_SUBST, using string.Template as
# substitution machinery (substituting ${bindir} instead of AC's
# @bindir@).

# subclass install_data (which does the installation work), and
# redirect all ".ac_subst" files to make a substitution hop over the
# builddir.

class install_data_like_ac_subst(install_data):
    AC_SUBST_EXT = '.ac_subst'

    def initialize_options(self):
        self.bindir = None
        self.libdir = None
        self.builddir = None
        self.sharedir = None
        super().initialize_options()

    def finalize_options(self):
        super().finalize_options()
        self.set_undefined_options('install', ('install_scripts', 'bindir'))
        self.set_undefined_options('install', ('install_lib', 'libdir'))
        self.set_undefined_options('build', ('build_base', 'builddir'))
        self.set_undefined_options('install', ('install_data', 'sharedir'))
        self.builddir = os.path.join(self.builddir, 'data_like_ac_subst')
        self.sharedir = os.path.join(self.sharedir, 'share')
        
    def run(self):
        data_files = []
        for f in self.data_files:
            # "what could f be?" answer taken from
            # distutils.command.install_data.run ...
            if isinstance(f, str):
                # a plain filename, to be installed right into
                # ${prefix}
                data_files.append(self._maybe_ac_subst(f))
            else:
                # tuple with path to install to and a list of files
                data_files.append((f[0], [self._maybe_ac_subst(ff) for ff in f[1]]))

        self.data_files = data_files
        super().run()

    def _maybe_ac_subst(self, filename):
        if not filename.endswith(self.AC_SUBST_EXT):
            return filename

        with open(filename) as f:
            template = string.Template(f.read())

        content = template.substitute({
            'bindir': self.bindir,
            'libdir': self.libdir,
            'sharedir': self.sharedir,
        })

        rel_dirname, src_filename = os.path.split(filename)
        build_dirname = os.path.join(self.builddir, rel_dirname)
        build_filename, _ = os.path.splitext(src_filename)
        build_filename = os.path.join(build_dirname, build_filename)

        os.makedirs(build_dirname, exist_ok=True)
        with open(build_filename, 'w') as f:
            f.write(content)

        return build_filename

setup(
    cmdclass={'install_data': install_data_like_ac_subst},
    name="openheating",
    license="GPLv3",
    url="http://openheating.org",
    version='0',
    description="Heating control",
    author="Joerg Faschingbauer",
    author_email="jf@faschingbauer.co.at",

    packages=[
        'openheating',
        'openheating.base',
        'openheating.test',
        'openheating.dbus',
        'openheating.web',
    ],

    data_files=[
        ('share/systemd',
         [
             'systemd/openheating-errors.service.ac_subst',
             'systemd/openheating-http.service.ac_subst',
             'systemd/openheating-thermometers.service.ac_subst',
         ]
        ),

        ('share/dbus',
         [
             # system dbus policies
             'dbus/org.openheating.conf',
         ]
        ),

        ('share/installations/faschingbauer',
         [
             'installations/faschingbauer/thermometers.pyconf',
         ]
        ),

        ('share/web/static/icons/www.opensecurityarchitecture.org',
         [
             'openheating/web/static/icons/www.opensecurityarchitecture.org/osa_home.svg',
             'openheating/web/static/icons/www.opensecurityarchitecture.org/osa_ics_drive.svg',
             'openheating/web/static/icons/www.opensecurityarchitecture.org/osa_ics_thermometer.svg',
             'openheating/web/static/icons/www.opensecurityarchitecture.org/osa_warning.svg',
         ],
        ),

        ('share/web/static',
         [
             'openheating/web/static/small.css',
         ],
        ),

        ('share/web/templates',
         [
             'openheating/web/templates/base.html',
             'openheating/web/templates/errors.html',
             'openheating/web/templates/history_macros.html',
             'openheating/web/templates/faschingbauer_home.html',
             'openheating/web/templates/thermometer.html',
             'openheating/web/templates/thermometers.html',
         ],
        ),

    ],
    scripts=[
        'bin/openheating-http.py',
        'bin/openheating-thermometers.py',
        'bin/openheating-errors.py',

        'bin/openheating-w1-list.py',
    ],
)
