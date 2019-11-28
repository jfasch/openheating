from openheating.base import pyconf
from openheating.test import testutils

import unittest


class SwitchesConfigTest(unittest.TestCase):
    def test_basic(self):
        switches = pyconf.read_switches([
            'from openheating.base.switch import DummySwitch',
            'SWITCHES = [',
            '    DummySwitch("name", "description", True)',
            ']',
        ])
        self.assertEqual(len(switches), 1)
        self.assertEqual(switches[0].name, 'name')

    def test__duplicate(self):
        with self.assertRaises(pyconf.DuplicateError) as what:
            pyconf.read_switches([
                'from openheating.base.switch import DummySwitch',
                'SWITCHES = [',
                '    DummySwitch("name", "description", True),',
                '    DummySwitch("name", "description", True),',
                ']',
            ])

        self.assertEqual(what.exception.name, 'name')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesConfigTest)

if __name__ == '__main__':
    testutils.run(suite)
