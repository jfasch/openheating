from openheating.dbus import names
from openheating.plant import plant
from openheating.plant import locations
from openheating.plant import service_unit
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils

from configparser import ConfigParser
import os
import os.path
import subprocess
import unittest


class SystemdGeneratorTest(PlantTestCase):
    def setUp(self):
        super().setUp()

        self.__plant_configfile = self.tempfile(
            lines=[
                'from openheating.plant.service_def import ThermometerService',
                'from openheating.plant.service_def import SwitchService',
                'from openheating.plant.service_def import CircuitService',
                'from openheating.plant.service_def import ErrorService',

                'from openheating.plant import locations',

                'ADD_SERVICE(ThermometerService(',
                '    config = locations.confdir + "/thermometers.pyconf"))',
                'ADD_SERVICE(SwitchService(',
                '    config = locations.confdir + "/switches.pyconf"))',
                'ADD_SERVICE(CircuitService(',
                '    config = locations.confdir + "/circuits.pyconf"))',
                'ADD_SERVICE(ErrorService())',
            ],
            suffix='.plant-config',
        )

    @PlantTestCase.intercept_failure
    def test__servicedef_to_unit_string(self):
        the_plant = plant.create_plant_with_main(self.__plant_configfile.name)

        for s in the_plant.servicedefs:
            content  = service_unit.create(
                s, sourcepath=self.__plant_configfile.name, generator_exe=__name__)
            config = ConfigParser()
            config.read_string(content)

            self.assertEqual(len(config['Unit']), 2)
            self.assertEqual(config['Unit']['Description'], s.description)
            self.assertEqual(config['Unit']['SourcePath'], self.__plant_configfile.name)
            self.assertEqual(len(config['Service']), 5)
            self.assertEqual(config['Service']['User'], 'openheating')
            self.assertEqual(config['Service']['Environment'], 'PYTHONPATH='+locations.libdir)
            self.assertEqual(config['Service']['Type'], 'dbus')
            self.assertEqual(config['Service']['BusName'], s.busname)
            self.assertEqual(len(config['Install']), 1)
            self.assertEqual(config['Install']['WantedBy'], 'multi-user.target')

            l = config['Service']['ExecStart'].split()
            self.assertEqual(l[0], os.path.join(locations.bindir, s.exe))
            args = l[1:]

            # in the remainder, we successively chew off the checked
            # commandline arguments, until there is nothing left.
            i = args.index('--system')
            del args[i]

            if s.busname == names.Bus.THERMOMETERS:
                self.assertEqual(len(s.wants), 0)
                i = args.index('--config')
                del args[i]
                self.assertEqual(args[i], locations.confdir + '/thermometers.pyconf')
                del args[i]
            elif s.busname == names.Bus.MAIN:
                self.assertEqual(len(s.wants), 4)
                self.assertIn('openheating-thermometers.service', s.wants)
                self.assertIn('openheating-switches.service', s.wants)
                self.assertIn('openheating-circuits.service', s.wants)
                self.assertIn('openheating-errors.service', s.wants)
                i = args.index('--config')
                del args[i]
                self.assertEqual(args[i], self.__plant_configfile.name)
                del args[i]
            elif s.busname == names.Bus.SWITCHES:
                self.assertEqual(len(s.wants), 0)
                i = args.index('--config')
                del args[i]
                self.assertEqual(args[i], locations.confdir + '/switches.pyconf')
                del args[i]
            elif s.busname == names.Bus.CIRCUITS:
                self.assertEqual(len(s.wants), 2)
                self.assertIn('openheating-thermometers.service', s.wants)
                self.assertIn('openheating-switches.service', s.wants)
                i = args.index('--config')
                del args[i]
                self.assertEqual(args[i], locations.confdir + '/circuits.pyconf')
                del args[i]
            elif s.busname == names.Bus.ERRORS:
                self.assertEqual(len(s.wants), 0)
                pass
            else:
                self.fail('unexpected busname '+s.busname)

            self.assertEqual(len(args), 0)

    @PlantTestCase.intercept_failure
    def test__generator_writes_service_unit_files(self):
        normal_dir, early_dir, late_dir = self.tempdir(), self.tempdir(), self.tempdir()
        genexe = locations.find_executable('openheating-systemd-generator.py.in')
        completed = subprocess.run([genexe, '--config', self.__plant_configfile.name, 
                                    normal_dir.name, early_dir.name, late_dir.name])
        self.assertEqual(completed.returncode, 0)

        # we know that the generator uses normal-dir; check if he put
        # the unit files there.
        main_unit = os.path.join(normal_dir.name, 'openheating-main.service')
        thermometers_unit = os.path.join(normal_dir.name, 'openheating-thermometers.service')
        switches_unit = os.path.join(normal_dir.name, 'openheating-switches.service')
        circuits_unit = os.path.join(normal_dir.name, 'openheating-circuits.service')
        errors_unit = os.path.join(normal_dir.name, 'openheating-errors.service')

        self.assertTrue(os.path.isfile(main_unit))
        self.assertTrue(os.path.isfile(thermometers_unit))
        self.assertTrue(os.path.isfile(switches_unit))
        self.assertTrue(os.path.isfile(circuits_unit))
        self.assertTrue(os.path.isfile(errors_unit))

        # all units are "WantedBy" the multiuser target; this is
        # stated by the respective symlinks in a subdir of normal-dir.
        wants_dir = os.path.join(normal_dir.name, 'multi-user.target.wants')
        self.assertTrue(os.path.isdir(wants_dir))

        main_link = os.path.join(wants_dir, 'openheating-main.service')
        thermometers_link = os.path.join(wants_dir, 'openheating-thermometers.service')
        switches_link = os.path.join(wants_dir, 'openheating-switches.service')
        circuits_link = os.path.join(wants_dir, 'openheating-circuits.service')
        errors_link = os.path.join(wants_dir, 'openheating-errors.service')

        self.assertTrue(os.path.islink(main_link))
        self.assertTrue(os.path.islink(thermometers_link))
        self.assertTrue(os.path.islink(switches_link))
        self.assertTrue(os.path.islink(circuits_link))
        self.assertTrue(os.path.islink(errors_link))

        # "WantedBy" links point to the generated units
        self.assertEqual(os.readlink(main_link), main_unit)
        self.assertEqual(os.readlink(thermometers_link), thermometers_unit)
        self.assertEqual(os.readlink(switches_link), switches_unit)
        self.assertEqual(os.readlink(circuits_link), circuits_unit)
        self.assertEqual(os.readlink(errors_link), errors_unit)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SystemdGeneratorTest))

if __name__ == '__main__':
    testutils.run(suite)

