from openheating.logic.brain import Brain
from openheating.logic.thinker import LeafThinker, CompositeThinker

from abc import ABCMeta, abstractmethod
import unittest
import logging

class _MyThinker(LeafThinker, metaclass=ABCMeta):
    def __init__(self, name):
        LeafThinker.__init__(self, name)
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

        thinker = MyThinker('my-thinker')
        brain = Brain([thinker])

        brain.think()

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

        thinker = MyThinker('my-thinker')
        brain = Brain([thinker])

        brain.think()

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

        thinker = MyThinker('my-thinker')
        brain = Brain([thinker], max_loop=10)

        self.assertRaises(brain.InfiniteLoop, brain.think)

        self.assertEqual(thinker.num_init_local, 1)
        self.assertEqual(thinker.num_init_global, 1)
        self.assertEqual(thinker.num_think, 10)

        # note that, although think() raises InfiniteLoop, we
        # insist in finish being called
        self.assertEqual(thinker.num_finish_local, 1)
        self.assertEqual(thinker.num_finish_global, 1)

    def test__composite_thinker(self):
        '''composite thinker'''

        class Single(_MyThinker):
            def do_think(self):
                return 0

        single = Single('single')
        composite = CompositeThinker('comp', [single])
        brain = Brain(thinkers=[composite])

        brain.think()

        self.assertEqual(single.num_init_local, 1)
        self.assertEqual(single.num_init_global, 1)
        self.assertEqual(single.num_think, 1)
        self.assertEqual(single.num_finish_local, 1)
        self.assertEqual(single.num_finish_global, 1)

    def test__composite_thinker__recursive(self):
        '''composite thinkers are expanded, recursively'''

        class Single(_MyThinker):
            def do_think(self):
                return 0

        single = Single('leaf')
        inner = CompositeThinker('inner', [single])
        outer = CompositeThinker('outer', [inner])
        brain = Brain(thinkers=[outer])

        brain.think()

        self.assertEqual(single.num_init_local, 1)
        self.assertEqual(single.num_init_global, 1)
        self.assertEqual(single.num_think, 1)
        self.assertEqual(single.num_finish_local, 1)
        self.assertEqual(single.num_finish_global, 1)

    def test__brain_duplicate_thinkers(self):
        '''when thinkers are expanded, there must be no duplicates'''
        
        class MyThinker(_MyThinker):
            def do_think(self): pass
        single = MyThinker('single')

        # Brain ctor: duplicate detection at the top level
        self.assertRaises(Brain.DuplicateThinker, Brain, [single, single])
            
        # Brain ctor: duplicate detection when nested inside composites
        self.assertRaises(Brain.DuplicateThinker, Brain, [CompositeThinker('composite', [single, single])])
        self.assertRaises(Brain.DuplicateThinker, Brain, [CompositeThinker('composite', [single]), CompositeThinker('composite', [single])])
        

        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BrainTest))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
