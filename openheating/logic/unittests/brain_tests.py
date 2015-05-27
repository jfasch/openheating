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
                return []

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
                    ret = [(self.name(), 'one more thought')]
                else:
                    # already called, don't call me anymore
                    ret = []
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
                return [(self.name(), 'yet another thought')]

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
                return []

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
                return []

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

    def test__thinker_return_format(self):
        class Single(_MyThinker):
            def do_think(self):
                return [(self.name(), 'some message')]

        composite = CompositeThinker('composite', [Single('single1'), Single('single2')])
        thoughts = composite.think()
        
        self.assertEqual(thoughts, [('single1', 'some message'), ('single2', 'some message')])

    def test__thinker_brain_format(self):
        class Single(_MyThinker):
            def __init__(self, name, message, num_loop):
                _MyThinker.__init__(self, name)
                self.__message = message
                self.__num_loop = num_loop
            def do_think(self):
                if self.num_think < self.__num_loop:
                    return [(self.name(), self.__message)]
                else:
                    return []

        brain = Brain([Single('single', 'message', 3)])
        result = brain.think()

        self.assertEqual(result, [(0, [('single', 'message')]), (1, [('single', 'message')])])
        # a(ia(ss))
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BrainTest))

# print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
# suite.addTest(BrainTest('test__thinker_brain_format'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
