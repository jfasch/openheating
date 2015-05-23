from openheating.logic.brain import Brain
from openheating.logic.thinker import Thinker

from abc import ABCMeta, abstractmethod
import unittest
import logging

class _MyThinker(Thinker, metaclass=ABCMeta):
    def __init__(self, name):
        Thinker.__init__(self, name)
        self.num_init_local = 0
        self.num_finish_local = 0
        self.num_think = 0
        self.num_init_global = 0
        self.num_finish_global = 0
    def init_thinking_local(self):
        self.num_init_local += 1
    def init_thinking_global(self):
        self.num_init_global += 1
    def think(self):
        self.num_think += 1
        return self.do_think()
    def finish_thinking_global(self):
        self.num_finish_global += 1
    def finish_thinking_local(self):
        self.num_finish_local += 1

    @abstractmethod
    def do_think(self):
        assert False, 'abstract'


class BrainTest(unittest.TestCase):
    def test__think_simple(self):
        '''thinker's init/think/finish hooks are called'''

        class MyThinker(_MyThinker):
            def do_think(self):
                return 0

        brain = Brain()
        thinker = MyThinker('my-thinker')
        brain.register_thinker(thinker)

        brain.think('')

        self.assertEqual(thinker.num_init_local, 1)
        self.assertEqual(thinker.num_init_global, 1)
        self.assertEqual(thinker.num_think, 1)
        self.assertEqual(thinker.num_finish_local, 1)
        self.assertEqual(thinker.num_finish_global, 1)

    def test__think_repeatedly(self):
        '''thinkers think until there's nothing more to do'''
        
        class MyThinker(_MyThinker):
            def do_think(self):
                if self.num_think == 0:
                    # not yet called. force one next round
                    ret = 1
                else:
                    # already called, don't call me anymore
                    ret = 0
                self.num_think += 1
                return ret

        brain = Brain()
        thinker = MyThinker('my-thinker')
        brain.register_thinker(thinker)

        brain.think('')

        self.assertEqual(thinker.num_init_local, 1)
        self.assertEqual(thinker.num_init_global, 1)
        self.assertEqual(thinker.num_think, 2)
        self.assertEqual(thinker.num_finish_local, 1)
        self.assertEqual(thinker.num_finish_global, 1)

    def test__think_indefinitely(self):
        '''thinkers must think excessively (loop detection)'''

        class MyThinker(_MyThinker):
            # think and think and think ...
            def do_think(self):
                return 1

        brain = Brain(max_loop=10)
        thinker = MyThinker('my-thinker')
        brain.register_thinker(thinker)

        self.assertRaises(brain.InfiniteLoopError, brain.think, '')

        self.assertEqual(thinker.num_init_local, 1)
        self.assertEqual(thinker.num_init_global, 1)
        self.assertEqual(thinker.num_think, 10)

        # note that, although think() raises InfiniteLoopError, we
        # insist in finish being called
        self.assertEqual(thinker.num_finish_local, 1)
        self.assertEqual(thinker.num_finish_global, 1)
        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BrainTest))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
