from openheating.logic.thinker import LeafThinker
from openheating.logic.brain import Brain
from openheating.logic.looper import Looper

import unittest
import logging


class _Thinker(LeafThinker):
    def __init__(self, name, message):
        LeafThinker.__init__(self, name)
        self.__message = message
    def think(self):
        if self.__message is None:
            return []
        else:
            rv = [(self.name(), self.__message)]
            self.__message = None
            return rv

class _Trigger(Looper.Trigger):
    def __init__(self):
        self.num_triggered = 0
    def trigger(self):
        self.num_triggered += 1


class LooperTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain([_Thinker('thinker1', 'message1'), _Thinker('thinker2', 'message2')])
        trigger = _Trigger()
        looper = Looper(brain=brain, triggers=[trigger])

        for i in range(5):
            looper.loop()

        self.assertEqual(looper.num_loops(), 5)
        self.assertEqual(trigger.num_triggered, 5)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LooperTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
