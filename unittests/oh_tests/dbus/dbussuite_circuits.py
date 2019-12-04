from openheating.dbus.circuit_center import CircuitCenter_Client

from openheating.test import services
from openheating.test import testutils

import pydbus

import unittest


class CircuitsTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([
            services.CircuitService(pyconf=[
                'from openheating.base.circuit import Circuit',
                'from openheating.base.thermometer import FixedThermometer',
                'from openheating.base.switch import DummySwitch',

                'producer = FixedThermometer("producer", "producer", 42)',
                'consumer = FixedThermometer("consumer", "consumer", 20)',
                'pump = DummySwitch("pump", "pump", False)',

                'CIRCUITS = [',
                '   Circuit("TestCircuit", "Test Circuit", pump=pump, producer=producer, consumer=consumer, diff_low=3, diff_high=10)',
                ']',
            ]),
        ])

    def test__basic(self):
        center_client = CircuitCenter_Client(pydbus.SessionBus())
        circuit_client = center_client.get_circuit('TestCircuit')
        self.assertEqual(circuit_client.get_name(), 'TestCircuit')
        self.assertEqual(circuit_client.get_description(), 'Test Circuit')

        circuit_client.activate()
        self.assertTrue(circuit_client.is_active())

        circuit_client.deactivate()
        self.assertFalse(circuit_client.is_active())

    def test__pump_on_off(self):
        self.fail('file switches, file thermometers')

    def test__notifications(self):
        self.fail('pump on/off, activated')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

