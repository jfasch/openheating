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
        super().__init__(
            [
                service.ThermometerService(
                    simulation_dir=make_tempdir(suffix='.thermometers').name,
                    background_updates=False,
                    config=make_tempfile(
                        lines=[
                            'from openheating.base.thermometer import FileThermometer',

                            'ADD_THERMOMETER("consumer", "the consumer")',
                            'ADD_THERMOMETER("producer", "the producer")',
                            # suppress periodic temperature reads; we
                            # inject
                        ],
                        suffix='.thermometers-config',
                    ).name),
                
                service.SwitchService(
                    simulation_dir=make_tempdir(suffix='.switches').name,
                    config=make_tempfile(
                        lines=[
                            'from openheating.base.switch import FileSwitch',
                            'ADD_SWITCH("pump", "the pump")',
                        ],
                        suffix='.switches-config'
                    ).name),
                
                service.CircuitService(
                    config=make_tempfile(
                        lines=[
                            'from openheating.base.circuit import Circuit',
                            'from openheating.dbus.thermometer_center import ThermometerCenter_Client',
                            'from openheating.dbus.switch_center import SwitchCenter_Client',

                            'thermometer_center = ThermometerCenter_Client(bus=GET_BUS())',
                            'switch_center = SwitchCenter_Client(bus=GET_BUS())',
                            'consumer_thermometer = thermometer_center.get_thermometer("consumer")',
                            'producer_thermometer = thermometer_center.get_thermometer("producer")',
                            'pump_switch = switch_center.get_switch("pump")',

                            'ADD_CIRCUIT("TestCircuit", "Test Circuit",',
                            '            Circuit(pump=pump_switch, producer=producer_thermometer, consumer=consumer_thermometer,',
                            '                    diff_low=3, diff_high=10,',
                            '                    debugstr="testcircuit")',
                            ')',
                        ],
                        suffix='.circuits-config',
                    ).name),
            ])
