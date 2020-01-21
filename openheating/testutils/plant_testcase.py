from . import testutils

from ..base.error import HeatingError
from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..plant.service import Service
from ..plant import dbusutil

import pydbus

import tempfile
import unittest


class PlantTestCase(unittest.TestCase):
    '''TestCase derivative which is good at managing dbus services as
    subprocesses.

    If failure is detected (see the intercept_failure() decorator),
    then at tearDown the stderr output of each service is printed.

    '''

    @staticmethod
    def intercept_failure(testmethod):
        '''test method decorator to intercept test case failures (these are
        hard to come by otherwise)

        '''
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return testmethod(*args, **kwargs)
            except:
                self.__failure = True
                raise
        return wrapper

    def setUp(self):
        self.__is_failure = False
        self.__plant = None
        self.__tempdirs = []
        self.__tempfiles = []
        self.__bus = None
    def tearDown(self):
        if self.__plant:
            self.__plant.shutdown(print_stderr=self.__is_failure)
        for d in self.__tempdirs:
            d.cleanup()
        for f in self.__tempfiles:
            f.close()

    def start_plant(self, plant):
        self.__plant = plant
        self.__plant.startup(find_exe=testutils.find_executable, 
                             bus_kind=dbusutil.BUS_KIND_SESSION,
                             common_args=['--log-level', 'debug'])

    def stop_plant(self):
        assert self.__plant is not None
        self.__plant.shutdown(print_stderr=False)
        self.__plant = None

    def tempdir(self, suffix=None):
        d = tempfile.TemporaryDirectory(prefix=self.__class__.__name__, suffix=suffix)
        self.__tempdirs.append(d)
        return d
        
    def tempfile(self, lines=None, suffix=None):
        f = tempfile.NamedTemporaryFile(prefix=self.__class__.__name__, suffix=suffix, mode='w')
        self.__tempfiles.append(f)
        if lines is not None:
            f.write('\n'.join(lines))
            f.flush()
        return f

    @property
    def bus(self):
        if self.__bus is None:
            self.__bus = pydbus.SessionBus()
        return self.__bus

    def get_thermometer_client(self, name):
        '''Get a client object for a thermometer with name'''
        center = ThermometerCenter_Client(self.bus)
        return center.get_thermometer(name)

    def force_temperature_update(self, timestamp):
        '''Via DBus client, force an update of all thermometers'''
        client = ThermometerCenter_Client(self.bus)
        client.force_update(timestamp)
