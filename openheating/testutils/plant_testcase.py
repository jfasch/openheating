from . import testutils

from ..base.error import HeatingError
from ..base.thermometer import FileThermometer
from ..base.switch import FileSwitch
from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..dbus.circuit_center import CircuitCenter_Client
from ..plant.service import Service, ThermometerService, SwitchService
from ..plant import dbusutil

import pydbus

import os.path
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

        # we do extra stuff with those, like maintain tempdirs, and
        # provide convenience methods for tests
        self.__thermometer_service = None
        self.__switch_service = None

    def tearDown(self):
        if self.__plant:
            self.__plant.shutdown(print_stderr=self.__is_failure)
        for d in self.__tempdirs:
            d.cleanup()
        for f in self.__tempfiles:
            f.close()

        self.__thermometer_service = None
        self.__switch_service = None

    def start_plant(self, plant):
        self.__plant = plant
        self.__plant.startup(find_exe=testutils.find_executable, 
                             bus_kind=dbusutil.BUS_KIND_SESSION,
                             common_args=['--log-level', 'debug'])

        for s in self.__plant.running_services:
            if isinstance(s, ThermometerService):
                self.__thermometer_service = s
            if isinstance(s, SwitchService):
                self.__switch_service = s
            
    def stop_plant(self):
        assert self.__plant is not None
        self.__plant.shutdown(print_stderr=False)
        self.__plant = None
        self.__thermometer_service = None
        self.__switch_service = None

    def tempdir(self, suffix=None):
        d = tempfile.TemporaryDirectory(prefix=self.__class__.__name__+'.', suffix=suffix)
        self.__tempdirs.append(d)
        return d
        
    def tempfile(self, lines=None, suffix=None):
        f = tempfile.NamedTemporaryFile(prefix=self.__class__.__name__+'.', suffix=suffix, mode='w')
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

    def set_temperature_file_and_update(self, name, value, timestamp):
        '''Write temperature of thermometer 'name' to associated simulation
        file. Force an update on the dbus themometer object associated
        with 'name', so the current temperature is available for
        subsequent reads.

        '''
        self.assertIsNotNone(self.__thermometer_service)
        self.assertIsNotNone(self.__thermometer_service.simulation_dir)

        # modify temperature
        thfile = os.path.join(self.__thermometer_service.simulation_dir, name)
        self.assertTrue(os.path.isfile(thfile))
        FileThermometer(thfile).set_temperature(value)

        # force service to do an update
        self.__thermometer_service.thermometer_client(self.bus, name).force_update(timestamp)

    def set_temperature_files_and_update(self, namevaluedict, timestamp):
        ''''namevaluedict' is a dictionary { 'name': float(value) },
        containing values to be written to the associated simulation
        files. Write those, and force-update all relevant dbus
        thermometer objects so the current temperature is available
        for subsequent reads.

        '''
        for name, value in namevaluedict.items():
            self.set_temperature_file_and_update(name, value, timestamp)

    def get_temperature_dbus(self, name):
        '''Over dbus, get the current temperature of the dbus object
        associated with 'name'.

        '''
        self.assertIsNotNone(self.__thermometer_service)
        return self.__thermometer_service.thermometer_client(self.bus, name).get_temperature()

    def force_temperature_update(self, timestamp):
        '''Via DBus client, force an update of all thermometers'''
        client = ThermometerCenter_Client(self.bus)
        client.force_update(timestamp)

    def get_switchstate_dbus(self, name):
        '''Talking to the dbus object associated with 'name', get the switch
        state.
        '''
        self.assertIsNotNone(self.__switch_service)
        return self.__switch_service.switch_client(self.bus, name).get_state()

    def set_switchstate_dbus(self, name, value):
        '''Talking to the dbus object associated with 'name', set the switch
        state.

        '''
        self.assertIsNotNone(self.__switch_service)
        self.__switch_service.switch_client(self.bus, name).set_state(value)

    def get_switchstate_file(self, name):
        '''Reading the switch-file associated with 'name', get the switch
        state.

        '''
        self.assertIsNotNone(self.__switch_service)
        self.assertIsNotNone(self.__switch_service.simulation_dir)
        return FileSwitch(os.path.join(self.__switch_service.simulation_dir, name)).get_state()

    def set_switchstate_file(self, name, value):
        '''Writing the switch-file associated with 'name', set the switch
        state.

        '''
        self.assertIsNotNone(self.__switch_service)
        self.assertIsNotNone(self.__switch_service.simulation_dir)
        FileSwitch(os.path.join(self.__switch_service.simulation_dir, name)).set_state(value)

    def activate_circuit(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).activate()

    def deactivate_circuit(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).deactivate()

    def is_circuit_active(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).is_active()

    def poll_circuit(self, name, timestamp):
        return CircuitCenter_Client(self.bus).get_circuit(name).poll(timestamp=timestamp)
