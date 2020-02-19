#!/usr/bin/python3


from distutils.core import setup
from distutils.cmd import Command
from distutils.dist import Distribution
from distutils.command.install_data import install_data
from distutils.command.build import build

import os
import string
import stat


# AC_SUBST taken from autoconf, basically, as follows:

# * setup(): specify a 'ac_subst' parameter, defining what file is
#   AC_SUBST'ed onto what file. (crap: I'd want to pass an 'ac_subst'
#   parameter to setup() but distutils won't let me -> subclass
#   'Distribution', and pass that class to setup() as 'distclass')

# * ac_subst_generate: a distutils Command class that does the
#   job. register that as first subcommand of the 'build' command, so
#   it is run automatically. crap: generates files into the source
#   tree (there is no easy other way)

# * cleanup of generated files: crap: I'd like to register an
#   ac_subst_cleanup command as the last command of the build, but
#   this is too early for install_data (and likely others). solution:
#   class dist.cleanup() explicitly, after setup() returns.

class ac_subst_generate(Command):
    def initialize_options(self):
        self.bindir = None
        self.libdir = None
        self.sharedir = None

    def finalize_options(self):
        self.set_undefined_options('install', ('install_scripts', 'bindir'))
        self.set_undefined_options('install', ('install_lib', 'libdir'))
        self.set_undefined_options('install', ('install_data', 'sharedir'))
        self.sharedir = os.path.join(self.sharedir, 'share')

    def run(self):
        for infile, outfile in self.distribution.ac_subst:
            with open(infile) as f:
                template = string.Template(f.read())
            with open(outfile, 'w') as f:
                f.write(template.substitute({
                    'bindir': self.bindir,
                    'libdir': self.libdir,
                    'sharedir': self.sharedir,
                    'webdir': os.path.join(self.sharedir, 'web'),
                }))
            
            # preserve mode and times of infile
            instat = os.stat(infile)
            os.utime(outfile, (instat[stat.ST_ATIME], instat[stat.ST_MTIME]))
            os.chmod(outfile, stat.S_IMODE(instat[stat.ST_MODE]))

build.sub_commands.insert(0, ('ac_subst_generate', lambda _: True))


class MyDistribution(Distribution):
    def __init__(self, attrs):
        ac_subst = attrs.get('ac_subst')  # [(infile, outfile)]
        if ac_subst is None:
            self.ac_subst = []
        else:
            del attrs['ac_subst']
            self.ac_subst = ac_subst

        super().__init__(attrs)

    def cleanup(self):
        for _, outfile in self.ac_subst:
            try:
                os.unlink(outfile)
            except FileNotFoundError: 
                pass


dist = setup(
    distclass = MyDistribution,
    cmdclass={
        'ac_subst_generate': ac_subst_generate,
    }, 
    name="openheating",
    license="GPLv3", url="http://openheating.org", version='0',
    description="Heating control", author="Joerg Faschingbauer",
    author_email="jf@faschingbauer.co.at",
    
    packages=[
        'openheating',
        'openheating.base',
        'openheating.testutils',
        'openheating.dbus',
        'openheating.plant',
        'openheating.web',
    ],
       
    data_files=[
        ('share/systemd',
         [
             'systemd/openheating-http.service',
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
             'installations/faschingbauer/switches.pyconf',
             'installations/faschingbauer/circuits.pyconf',
             'installations/faschingbauer/plant.pyconf',
             'installations/faschingbauer/config.txt',
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
             'openheating/web/templates/faschingbauer_home.html',
             'openheating/web/templates/thermometer.html',
             'openheating/web/templates/thermometers.html',
             'openheating/web/templates/circuits.html',
             'openheating/web/templates/switches.html',
             'openheating/web/templates/errors.html',
             'openheating/web/templates/history_macros.html',
         ],
        ),
    ],

    scripts=[
        # web server (dbus client)
        'bin/openheating-http.py',

        # somehing that can run a plant (obviously)
        'bin/openheating-runplant.py',

        # dbus components ("the plant")
        'bin/openheating-main.py',
        'bin/openheating-thermometers.py',
        'bin/openheating-switches.py',
        'bin/openheating-circuits.py',
        'bin/openheating-errors.py',

        # unit file generator
        'bin/openheating-systemd-generator.py',

        # w1 testing
        'bin/openheating-w1-list.py',
    ],

    ac_subst = [
        ('bin/openheating-systemd-generator.py.in',
         'bin/openheating-systemd-generator.py'),

        ('openheating/plant/installed.py.in',
         'openheating/plant/installed.py'),

        ('systemd/openheating-http.service.in',
         'systemd/openheating-http.service'),
    ],
)

dist.cleanup()
