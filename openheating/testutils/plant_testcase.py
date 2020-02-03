from . import testutils

from ..base.error import HeatingError
from ..base.thermometer import FileThermometer
from ..base.switch import FileSwitch
from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..dbus.switch_center import SwitchCenter_Client
from ..dbus.circuit_center import CircuitCenter_Client
from ..dbus.main import MainPollable_Client
from ..plant import dbusutil
from ..plant.service_def import ThermometerService
from ..plant.service_def import SwitchService

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
                self.__is_failure = True
                raise
        return wrapper

    def setUp(self):
        self.__is_failure = False
        self.__plant = None
        self.__tempdirs = []
        self.__tempfiles = []
        self.__bus = None

        # this is where thermometers and switches go. valid from
        # start_plant() (if called with simulation=True) to tearDown()
        self.__simulation_dir = None
        self.__thermometers_dir = None
        self.__switches_dir = None

    def tearDown(self):
        if self.__plant:
            self.__plant.shutdown(print_stderr=self.__is_failure)
        for d in self.__tempdirs:
            d.cleanup()
        for f in self.__tempfiles:
            f.close()

    @property
    def simulation_dir(self): return self.__simulation_dir
    @property
    def thermometers_dir(self): return self.__thermometers_dir
    @property
    def switches_dir(self): return self.__switches_dir
    
    def start_plant(self, plant, simulation=True):
        self.__plant = plant

        if simulation:
            # create simulation base directory, and tell plant about
            # it.
            self.__simulation_dir = self.tempdir(suffix='.simulation').name
            self.__thermometers_dir, self.__switches_dir = \
                self.__plant.enable_simulation_mode(simulation_dir=self.__simulation_dir)

        self.__plant.startup(
            find_exe=testutils.find_executable, 
            bus_kind=dbusutil.BUS_KIND_SESSION,
            common_args=['--log-level', 'debug'],
            # we print stderr on failure
            capture_stderr=True,
        )

    def stop_plant(self):
        assert self.__plant is not None
        self.__plant.shutdown(print_stderr=False)
        self.__plant = None

    def tempdir(self, suffix=None):
        d = tempfile.TemporaryDirectory(prefix='openheating-{}-'.format(self.__class__.__name__), suffix=suffix)
        self.__tempdirs.append(d)
        return d
        
    def tempfile(self, lines=None, suffix=None):
        f = tempfile.NamedTemporaryFile(prefix='openheating-{}-'.format(self.__class__.__name__), suffix=suffix, mode='w')
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

    def set_temperature_file_without_update(self, name, value):
        '''Write temperature of thermometer 'name' to associated simulation
        file. No update is kicked; that is left to the user.

        '''
        self.__set_temperature_file(name, value)

    def set_temperature_file_and_update(self, name, value, timestamp):
        '''Write temperature of thermometer 'name' to associated simulation
        file. Force an update on the dbus themometer object associated
        with 'name', so the current temperature is available for
        subsequent reads.

        '''
        self.assertIsNotNone(self.__thermometers_dir)

        self.__set_temperature_file(name, value)

        # force service to do an update
        self._create_thermometer_client(name).force_update(timestamp)

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
        return self._create_thermometer_client(name).get_temperature()

    def force_temperature_update(self, timestamp):
        '''Via DBus client, force an update of all thermometers'''
        self._create_thermometer_center_client().force_update(timestamp)

    def get_switchstate_dbus(self, name):
        '''Talking to the dbus object associated with 'name', get the switch
        state.
        '''
        return self._create_switch_client(name).get_state()

    def set_switchstate_dbus(self, name, value):
        '''Talking to the dbus object associated with 'name', set the switch
        state.

        '''
        return self._create_switch_client(name).set_state(value)

    def get_switchstate_file(self, name):
        '''Reading the switch-file associated with 'name', get the switch
        state.

        '''
        return FileSwitch(os.path.join(self.__switches_dir, name)).get_state()

    def set_switchstate_file(self, name, value):
        '''Writing the switch-file associated with 'name', set the switch
        state.

        '''
        FileSwitch(os.path.join(self.__switches_dir, name)).set_state(value)

    def activate_circuit(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).activate()

    def deactivate_circuit(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).deactivate()

    def is_circuit_active(self, name):
        return CircuitCenter_Client(self.bus).get_circuit(name).is_active()

    def poll_circuit(self, name, timestamp):
        return CircuitCenter_Client(self.bus).get_circuit(name).poll(timestamp=timestamp)

    def poll_main(self, timestamp):
        return MainPollable_Client(self.bus).poll(timestamp=timestamp)

    def __set_temperature_file(self, name, value):
        thfile = os.path.join(self.__thermometers_dir, name)
        self.assertTrue(os.path.isfile(thfile))
        FileThermometer(thfile).set_temperature(value)

    def _create_thermometer_center_client(self):
        return ThermometerCenter_Client(self.bus)

    def _create_thermometer_client(self, name):
        return self._create_thermometer_center_client().get_thermometer(name)
        
    def _create_switch_center_client(self):
        return SwitchCenter_Client(self.bus)

    def _create_switch_client(self, name):
        return self._create_switch_center_client().get_switch(name)
        
