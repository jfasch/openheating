from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.base.thermometer import FileThermometer
from openheating.base.switch import FileSwitch

from openheating.test import services
from openheating.test import testutils

import pydbus

import unittest
from tempfile import NamedTemporaryFile
import time


class CircuitsTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()

        # create and init thermometer and switch files
        self.__consumer_thermometer_file = NamedTemporaryFile(mode='w')
        self.__producer_thermometer_file = NamedTemporaryFile(mode='w')
        self.__pump_switch_file = NamedTemporaryFile(mode='w')

        self.__consumer_thermometer = FileThermometer('consumer', 'consumer', self.__consumer_thermometer_file.name)
        self.__producer_thermometer = FileThermometer('producer', 'producer', self.__producer_thermometer_file.name)
        self.__pump_switch = FileSwitch('pump', 'pump', self.__pump_switch_file.name)

        self.__consumer_thermometer.set_temperature(10)
        self.__producer_thermometer.set_temperature(10)
        self.__pump_switch.set_state(False)

        self.start_services(
            [
                services.ThermometerService(
                    pyconf=[
                        'from openheating.base.thermometer import FileThermometer',
                        
                        'THERMOMETERS = [',
                        '    FileThermometer("consumer", "the consumer", "'+self.__consumer_thermometer_file.name+'"),',
                        '    FileThermometer("producer", "the producer", "'+self.__producer_thermometer_file.name+'"),',
                        ']',
                    ],
                    update_interval=0),
                services.SwitchService(
                    pyconf=[
                        'from openheating.base.switch import FileSwitch',
                
                        'SWITCHES = [',
                        '    FileSwitch("pump", "the pump", "'+self.__pump_switch_file.name+'"),',
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

        circuite_center_client = CircuitCenter_Client(pydbus.SessionBus())
        self.__circuit_client = circuite_center_client.get_circuit('TestCircuit')
        self.assertEqual(self.__circuit_client.get_name(), 'TestCircuit')
        self.assertEqual(self.__circuit_client.get_description(), 'Test Circuit')

        thermometer_center_client = ThermometerCenter_Client(pydbus.SessionBus())
        self.__producer_thermometer_client = thermometer_center_client.get_thermometer('producer')
        self.__consumer_thermometer_client = thermometer_center_client.get_thermometer('consumer')

    def tearDown(self):
        self.__consumer_thermometer_file.close()
        self.__producer_thermometer_file.close()
        self.__pump_switch_file.close()

        super().tearDown()

    @services.ServiceTestCase.intercept_failure
    def test__activate_deactivate(self):
        self.__circuit_client.activate()
        self.assertTrue(self.__circuit_client.is_active())

        self.__circuit_client.deactivate()
        self.assertFalse(self.__circuit_client.is_active())

    # jjj
    
    # @services.ServiceTestCase.intercept_failure
    # def test__pump_on_off(self):
    #     # paranoia. we initialized the thermometers to give 10
    #     # degrees.
    #     self.assertAlmostEqual(self.__consumer_thermometer.get_temperature(), 10)
    #     self.assertAlmostEqual(self.__producer_thermometer.get_temperature(), 10)

    #     self.__circuit_client.activate()
    #     self.__circuit_client.poll(0) # epoch
    #     self.assertFalse(self.__pump_switch.get_state())

    #     self.__producer_thermometer.set_temperature(50)
    #     self.assertAlmostEqual(self.__producer_thermometer.get_temperature(), 50)

    #     # wait until thermometer service has seen the change.
    #     for _ in range(20):
    #         time.sleep(0.1)
    #         temp = self.__producer_thermometer_client.get_temperature()
    #         if 49.5 < temp < 50.5: # we set it to 50, and it is a
    #                                # float :-)
    #             break
    #     else:
    #         self.fail('temperature change not seen within timeout')

    #     self.__circuit_client.poll(10) # epoch+10
    #     self.assertTrue(self.__pump_switch.get_state())

    # def test__notifications(self):
    #     self.fail('pump on/off, activated')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

