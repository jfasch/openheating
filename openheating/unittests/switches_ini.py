from openheating.switches_ini import read_string
from openheating.switch import DummySwitch
from openheating.error import BadDBusPathComponent

import unittest


class SwitchesIniTest(unittest.TestCase):
    def test__basic(self):
        switches = read_string(
            """
            [PumpeWasserDummy]
            Type = dummy
            Description = Pumpe Warmwasserkreis
            State = True

            [PumpeHeizDummy]
            Type = dummy
            Description = Pumpe Heizkreis
            State = False

            [PumpeWasser]
            Type = gpio
            ChipLabel = pinctrl-bcm2835
            Offset = 21
            Direction = out
            Description = Pumpe Warmwasserkreis
            """,

            dummy=True
        )

        p = switches.get('PumpeWasserDummy')
        self.assertIsNotNone(p)
        self.assertTrue(isinstance(p, DummySwitch))
        self.assertTrue(p.get_state())
        self.assertEqual(p.name, 'PumpeWasserDummy')
        self.assertEqual(p.description, 'Pumpe Warmwasserkreis')

        p = switches.get('PumpeHeizDummy')
        self.assertIsNotNone(p)
        self.assertTrue(isinstance(p, DummySwitch))
        self.assertFalse(p.get_state())
        self.assertEqual(p.name, 'PumpeHeizDummy')
        self.assertEqual(p.description, 'Pumpe Heizkreis')

        p = switches.get('PumpeWasser')
        self.assertIsNotNone(p)
        self.assertFalse(p.get_state())
        self.assertEqual(p.name, 'PumpeWasser')
        self.assertEqual(p.description, 'Pumpe Warmwasserkreis')

    def test_bad_switch_name(self):
        self.assertRaises(BadDBusPathComponent, read_string,
            """
            [bad-name]
            Type = gpio
            """)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesIniTest)
