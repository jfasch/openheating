from openheating.base import pyconf
from openheating.test import testutils

import unittest


class SwitchesConfigTest(unittest.TestCase):
    def test__basic(self):
        switches = pyconf.read_switches([
            'from openheating.base.switch import DummySwitch',
            'SWITCHES = [',
            '    DummySwitch("name", "description", True)',
            ']',
        ])
        self.assertEqual(len(switches), 1)
        self.assertEqual(switches[0].get_name(), 'name')

    def test__duplicate(self):
        with self.assertRaises(pyconf.DuplicateName) as what:
            pyconf.read_switches([
                'from openheating.base.switch import DummySwitch',
                'SWITCHES = [',
                '    DummySwitch("name", "description", True),',
                '    DummySwitch("name", "description", True),',
                ']',
            ])

        self.assertEqual(what.exception.name, 'name')

    def test__bad_name(self):
        with self.assertRaises(pyconf.BadName) as what:
            pyconf.read_switches([
                'from openheating.base.switch import DummySwitch',
                'SWITCHES = [',
                '    DummySwitch("this is not an identifier", "description", True),',
                ']',
            ])

        self.assertEqual(what.exception.name, "this is not an identifier")

suite = unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesConfigTest)

if __name__ == '__main__':
    testutils.run(suite)
