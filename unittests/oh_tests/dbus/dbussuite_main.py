from openheating.plant import plant
from openheating.plant import config
from openheating.plant.service import PollWitnessService, MainService
from openheating.plant import simple_plant

from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils

import unittest
import time
import signal


class MainTest(PlantTestCase):
    def setUp(self):
        super().setUp()

        self.__poll_witness_file = self.tempfile(suffix='.poll-witness')
        self.__plant_config_file = self.tempfile(
            lines=[
                'from openheating.plant.service import PollWitnessService',
                'ADD_SERVICE(PollWitnessService(witness="{}"))'.format(self.__poll_witness_file.name),
            ],
            suffix='.plant-config')


    @PlantTestCase.intercept_failure
    def test__poll_main__check_witness__manual(self):
        # here we start a plant that corresponds to the plant
        # config. we do this manually, by replicating what's in the
        # config, and adding a main component on top of it.
        self.start_plant(plant.Plant([
            PollWitnessService(witness=self.__poll_witness_file.name),
            MainService(config=self.__plant_config_file.name)]))

        self.poll_main(timestamp=0)

        with open(self.__poll_witness_file.name) as f:
            s = f.read()
            timestamp = int(s)
            self.assertEqual(timestamp, 0)

    def test__poll_main__check_witness__automatic(self):
        # use a helper routine that creates a service list from the
        # plant config, adding all boilerplate like a main component
        # automatically
        self.start_plant(plant.create_plant_with_main(self.__plant_config_file.name))

        self.poll_main(timestamp=0)

        with open(self.__poll_witness_file.name) as f:
            s = f.read()
            timestamp = int(s)
            self.assertEqual(timestamp, 0)

class MainWithThermometersTest(PlantTestCase):
    def test__main_polls_thermometers(self):
        self.start_plant(simple_plant.create_with_main(
            make_tempfile=self.tempfile,
            make_tempdir=self.tempdir))

        # paranoia. see if thermometers have been read at startup, and
        # no "not initialized" exception is raised.
        self.get_temperature_dbus('producer')
        self.get_temperature_dbus('consumer')

        # set temperatures, *not* kicking the async update.
        self.set_temperature_file_without_update('producer', 42)
        self.set_temperature_file_without_update('consumer', 666)

        # poll once. Main will poll() Thermometers, kicking a
        # background thread to do the read asynchronously.
        self.poll_main(timestamp=42)

        # spin a while until the asynchronous read has made it onto
        # the surface.
        for _ in range(20):
            time.sleep(0.2)
            producer_temperature = self.get_temperature_dbus('producer')
            consumer_temperature = self.get_temperature_dbus('consumer')
            if abs(producer_temperature - 42) < 0.5 and abs(consumer_temperature - 666) < 0.5:  # almost equal
                break
        else:
            signal.pause()
            self.fail()
                
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainWithThermometersTest))

if __name__ == '__main__':
    testutils.run(suite)

