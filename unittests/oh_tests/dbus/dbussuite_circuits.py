from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.base.thermometer import FileThermometer
from openheating.base.switch import FileSwitch

from openheating.test import services
from openheating.test import testutils

import pydbus

import unittest


class CircuitsTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()

        # create and init thermometer and switch files
        self.__consumer_thermometer = FileThermometer.init_file(10)
        self.__producer_thermometer = FileThermometer.init_file(10)
        self.__pump_switch = FileSwitch.init_file(False)

        self.start_services([
            services.ThermometerService(pyconf=[
                'from openheating.base.thermometer import FileThermometer',
                
                'THERMOMETERS = [',
                '    FileThermometer("consumer", "the consumer", "'+self.__consumer_thermometer.name+'"),',
                '    FileThermometer("producer", "the producer", "'+self.__producer_thermometer.name+'"),',
                ']',
            ]),
            services.SwitchService(pyconf=[
                'from openheating.base.switch import FileSwitch',
                
                'SWITCHES = [',
                '    FileSwitch("pump", "the pump", "'+self.__pump_switch.name+'"),',
                ']',
            ]),
            services.CircuitService(pyconf=[
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
        ])

    def tearDown(self):
        self.__consumer_thermometer.close()
        self.__producer_thermometer.close()
        self.__pump_switch.close()

        super().tearDown()

    @services.ServiceTestCase.intercept_failure
    def test__basic(self):
        center_client = CircuitCenter_Client(pydbus.SessionBus())
        circuit_client = center_client.get_circuit('TestCircuit')
        self.assertEqual(circuit_client.get_name(), 'TestCircuit')
        self.assertEqual(circuit_client.get_description(), 'Test Circuit')

        circuit_client.activate()
        self.assertTrue(circuit_client.is_active())

        circuit_client.deactivate()
        self.assertFalse(circuit_client.is_active())

    # def test__pump_on_off(self):
    #     self.fail('file switches, file thermometers')

    # def test__poll(self):
    #     self.fail()

    # def test__notifications(self):
    #     self.fail('pump on/off, activated')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

