from . import service_def
from . import plant

from openheating.base.thermometer import FileThermometer
from openheating.base.switch import FileSwitch
from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.switch_center import SwitchCenter_Client

from collections import namedtuple

def create_without_main(make_tempfile, make_tempdir):
    thermometers_config, switches_config, circuits_config, _ = _configs(make_tempfile)

    return plant.Plant([
        service_def.ThermometerService(config=thermometers_config.name),
        service_def.SwitchService(config=switches_config.name),
        service_def.CircuitService(config=circuits_config.name),
    ])

def create_with_main(make_tempfile, make_tempdir):
    thermometers_config, switches_config, circuits_config, plant_config = _configs(make_tempfile)

    return plant.create_plant_with_main(plant_config.name)

def _configs(make_tempfile):
    thermometers_config = make_tempfile(
        lines=[
            'assert IS_SIMULATION',

            # this plant is supposed to only be
            # operated in simulation mode, so we don't
            # give real thermometers.
            'ADD_THERMOMETER("consumer", "the consumer", None)',
            'ADD_THERMOMETER("producer", "the producer", None)',
        ],
        suffix='.thermometers-config',
    )

    switches_config = make_tempfile(
        lines=[
            'from openheating.base.switch import FileSwitch',
            'assert IS_SIMULATION',
            'ADD_SWITCH("pump", "the pump", None)',
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

            'ADD_CIRCUIT("TestCircuit", "Test Circuit", Circuit,',
            '            pump=pump_switch, producer=producer_thermometer, consumer=consumer_thermometer,',
            '            diff_low=3, diff_high=10,',
            '            debugstr="testcircuit"',
            ')',
        ],
        suffix='.circuits-config',
    )

    plant_config = make_tempfile(
        lines=[
            'from openheating.plant.service_def import ThermometerService',
            'from openheating.plant.service_def import SwitchService',
            'from openheating.plant.service_def import CircuitService',

            'ADD_SERVICE(ThermometerService(',
            '    config = "{}",'.format(thermometers_config.name),
            '))',
            'ADD_SERVICE(SwitchService(',
            '    config = "{}",'.format(switches_config.name),
            '))',
            'ADD_SERVICE(CircuitService(',
            '    config = "{}"'.format(circuits_config.name),
            '))',
        ],
        suffix='.plant-config'
    )

    return thermometers_config, switches_config, circuits_config, plant_config
