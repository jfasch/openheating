from . import service
from .plant import Plant

from openheating.base.thermometer import FileThermometer
from openheating.base.switch import FileSwitch
from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.switch_center import SwitchCenter_Client

import pydbus

from collections import namedtuple


class SimplePlant(Plant):
    def __init__(self, bus, make_tempfile, make_tempdir):
        thermometers_dir = make_tempdir(suffix='.thermometers')
        switches_dir = make_tempdir(suffix='.switches')

        consumer_thermometer_file = thermometers_dir.name + '/consumer'
        producer_thermometer_file = thermometers_dir.name + '/producer'

        pump_switch_file = switches_dir.name + '/pump'

        # thermometers and switches for use by test code
        self.__consumer_thermometer = FileThermometer(path=consumer_thermometer_file)
        self.__producer_thermometer = FileThermometer(path=producer_thermometer_file)
        self.__pump_switch = FileSwitch(path=pump_switch_file)

        thermometers_config = make_tempfile(
            lines=[
                'from openheating.base.thermometer import FileThermometer',

                'ADD_THERMOMETER("consumer", "the consumer", FileThermometer(path="{}"))'.format(consumer_thermometer_file),
                'ADD_THERMOMETER("producer", "the producer", FileThermometer(path="{}"))'.format(producer_thermometer_file),
                # suppress periodic temperature reads; we
                # inject
                'SET_UPDATE_INTERVAL(0)',
            ],
            suffix='.thermometers-config',
        )

        switches_config = make_tempfile(
            lines=[
                'from openheating.base.switch import FileSwitch',
                'ADD_SWITCH("pump", "the pump", FileSwitch(path="{}", initial_value=False))'.format(pump_switch_file),
            ],
            suffix='.switches-config'
        )

        circuits_config = make_tempfile(
            lines=[
                'from openheating.base.circuit import Circuit',
                'from openheating.dbus.thermometer_center import ThermometerCenter_Client',
                'from openheating.dbus.switch_center import SwitchCenter_Client',

                'thermometer_center = ThermometerCenter_Client(bus=GET_BUS())',
                'switch_center = SwitchCenter_Client(bus=GET_BUS())',
                'consumer_thermometer = thermometer_center.get_thermometer("consumer")',
                'producer_thermometer = thermometer_center.get_thermometer("producer")',
                'pump_switch = switch_center.get_switch("pump")',

                'ADD_CIRCUIT(',
                '   Circuit("TestCircuit", "Test Circuit",',
                '           pump=pump_switch, producer=producer_thermometer, consumer=consumer_thermometer,',
                '           diff_low=3, diff_high=10)',
                ')',
            ],
            suffix='.circuits-config',
        )

        super().__init__(
            [
                service.ThermometerService(config=thermometers_config.name),
                service.SwitchService(config=switches_config.name),
                service.CircuitService(config=circuits_config.name),
            ])

    def create_clients(self):
        assert self.running

        clients = namedtuple('clients', ('circuit', 'producer_thermometer', 'consumer_thermometer', 'pump_switch'))

        circuit_center = CircuitCenter_Client(pydbus.SessionBus())
        circuit_client = circuit_center.get_circuit('TestCircuit')

        thermometer_center = ThermometerCenter_Client(pydbus.SessionBus())
        producer_thermometer = thermometer_center.get_thermometer('producer')
        consumer_thermometer = thermometer_center.get_thermometer('consumer')

        switch_center = SwitchCenter_Client(pydbus.SessionBus())
        pump_switch = switch_center.get_switch('pump')

        return clients(
            circuit=circuit_client,
            producer_thermometer=producer_thermometer,
            consumer_thermometer=consumer_thermometer,
            pump_switch=pump_switch)

    @property
    def consumer_file_thermometer(self):
        return self.__consumer_thermometer
    @property
    def producer_file_thermometer(self):
        return self.__producer_thermometer
    @property
    def pump_file_switch(self):
        return self.__pump_switch

    @property
    def consumer_dbus_thermometer(self):
        assert False
    @property
    def producer_dbus_thermometer(self):
        assert False
    @property
    def pump_dbus_switch(self):
        assert False
    @property
    def pump_dbus_circuit(self):
        assert False
