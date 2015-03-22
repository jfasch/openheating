from openheating.error import HeatingError
from openheating.testutils.test_switch import TestSwitch

from openheating.switch_center import SwitchCenter

import time
import unittest

class SwitchCenterTest(unittest.TestCase):
    def test_lookup(self):
        one = TestSwitch(name='one', initial_state=False)
        two = TestSwitch(name='two', initial_state=False)
        center = SwitchCenter({'one': one, 'two': two})
        center.do_close('one')
        self.assertTrue(one.is_closed())
        center.do_close('two')
        self.assertTrue(two.is_closed())
        center.do_open('one')
        self.assertTrue(one.is_open())
        center.do_open('two')
        self.assertTrue(two.is_open())

    def test_all_names(self):
        center = SwitchCenter({'one': TestSwitch(name='one', initial_state=False), 'two': TestSwitch(name='two', initial_state=False)})
        all_names = set(center.all_names())
        self.assertEqual(len(all_names), 2)
        self.assertIn('one', all_names)
        self.assertIn('two', all_names)

    def test_adapter_switch(self):
        one = TestSwitch(name='one', initial_state=False)
        two = TestSwitch(name='two', initial_state=False)
        center = SwitchCenter({'one': one, 'two': two})

        ad_one = center.get_switch('one')
        ad_two = center.get_switch('two')

        ad_one.do_close()
        ad_two.do_close()

        self.assertTrue(one.is_closed())
        self.assertTrue(two.is_closed())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchCenterTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
