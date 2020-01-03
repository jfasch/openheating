from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.switch_center import SwitchCenter_Client

from openheating.test import services
from openheating.test import testutils

import pydbus

import unittest
from tempfile import NamedTemporaryFile
import time
import itertools



class CircuitsTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()

        self.start_services(
            [
                services.ThermometerService(
                    pyconf=[
                        'from openheating.base.thermometer import DummyThermometer',
                        
                        'THERMOMETERS = [',
                        '    DummyThermometer("consumer", "the consumer", 0),',
                        '    DummyThermometer("producer", "the producer", 0),',
                        ']',
                    ],
                    update_interval=0),
                services.SwitchService(
                    pyconf=[
                        'from openheating.base.switch import DummySwitch',
                
                        'SWITCHES = [',
                        '    DummySwitch("pump", "the pump", False),',
                        ']',
                    ]),
                services.CircuitService(
                    pyconf=[
                        'from openheating.base.circuit import Circuit',
                        'from openheating.dbus.thermometer_center import ThermometerCenter_Client',
                        'from openheating.dbus.switch_center import SwitchCenter_Client',

                        'thermometer_center = ThermometerCenter_Client(bus=BUS)',
                        'switch_center = SwitchCenter_Client(bus=BUS)',
                        'consumer_thermometer = thermometer_center.get_thermometer("consumer")',
                        'producer_thermometer = thermometer_center.get_thermometer("producer")',
                        'pump_switch = switch_center.get_switch("pump")',
                        
                        'CIRCUITS = [',
                        '   Circuit("TestCircuit", "Test Circuit",',
                        '           pump=pump_switch, producer=producer_thermometer, consumer=consumer_thermometer,',
                        '           diff_low=3, diff_high=10)',
                        ']',
                    ]),
            ]
        )

        circuit_center = CircuitCenter_Client(pydbus.SessionBus())
        self.__circuit_client = circuit_center.get_circuit('TestCircuit')
        self.assertEqual(self.__circuit_client.get_name(), 'TestCircuit')
        self.assertEqual(self.__circuit_client.get_description(), 'Test Circuit')

        thermometer_center = ThermometerCenter_Client(pydbus.SessionBus())
        self.__producer_thermometer = thermometer_center.get_thermometer('producer')
        self.__consumer_thermometer = thermometer_center.get_thermometer('consumer')

        switch_center = SwitchCenter_Client(pydbus.SessionBus())
        self.__pump_switch = switch_center.get_switch('pump')

        # timestamps for injected samples
        self.__timeline = itertools.count()

        # provide initial values
        self.__producer_thermometer.inject_sample(timestamp=next(self.__timeline), temperature=10)
        self.__consumer_thermometer.inject_sample(timestamp=next(self.__timeline), temperature=10)
        self.__pump_switch.set_state(False)

    @services.ServiceTestCase.intercept_failure
    def test__activate_deactivate(self):
        self.__circuit_client.activate()
        self.assertTrue(self.__circuit_client.is_active())

        self.__circuit_client.deactivate()
        self.assertFalse(self.__circuit_client.is_active())

    @services.ServiceTestCase.intercept_failure
    def test__pump_on_off(self):
        # paranoia. we injected samples to give 10 degrees.
        self.assertAlmostEqual(self.__consumer_thermometer.get_temperature(), 10)
        self.assertAlmostEqual(self.__producer_thermometer.get_temperature(), 10)

        self.__circuit_client.activate()
        self.__circuit_client.poll(0) # epoch
        self.assertFalse(self.__pump_switch.get_state())

        # produce heat
        self.__producer_thermometer.inject_sample(timestamp=next(self.__timeline), temperature=50)
        # paranoia
        self.assertAlmostEqual(self.__producer_thermometer.get_temperature(), 50)

        self.__circuit_client.poll(next(self.__timeline))
        self.assertTrue(self.__pump_switch.get_state())

        # consume heat, but do not yet trigger hysteresis.
        self.__consumer_thermometer.inject_sample(timestamp=next(self.__timeline), temperature=45)
        # paranoia
        self.assertAlmostEqual(self.__consumer_thermometer.get_temperature(), 45)

        # pump still on (hysteresis lower bound is 3)
        self.__circuit_client.poll(next(self.__timeline))
        self.assertTrue(self.__pump_switch.get_state())
        
        # consume even more heat; difference goes below 3
        self.__consumer_thermometer.inject_sample(timestamp=next(self.__timeline), temperature=48)
        # paranoia
        self.assertAlmostEqual(self.__consumer_thermometer.get_temperature(), 48)

        # pump off
        self.__circuit_client.poll(next(self.__timeline))
        self.assertFalse(self.__pump_switch.get_state())
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

