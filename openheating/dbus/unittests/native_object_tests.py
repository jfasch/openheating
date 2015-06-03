from openheating.dbus.service_config_native import NativeObject

import unittest

class NativeObjectTest(unittest.TestCase):
    def test__instantiate_and_simple_call(self):
        class A:
            num_instantiations = 0
            num_calls = 0

            def __init__(self, member):
                A.num_instantiations += 1
                self.member = 1
            def f(self):
                A.num_calls += 1

        a = NativeObject(A, member=1)
        self.assertEqual(A.num_instantiations, 0)
        self.assertEqual(A.num_calls, 0)
        a.f()
        self.assertEqual(A.num_instantiations, 1)
        self.assertEqual(A.num_calls, 1)

    def test__call_with_base_lookup(self):
        class Base:
            num_instantiations = 0
            num_calls = 0
            def __init__(self):
                Base.num_instantiations += 1
            def base_method(self):
                Base.num_calls += 1
        class Derived(Base):
            pass

        derived = NativeObject(Derived)
        self.assertEqual(Base.num_instantiations, 0)
        self.assertEqual(Base.num_calls, 0)

        derived.base_method()
        self.assertEqual(Base.num_instantiations, 1)
        self.assertEqual(Base.num_calls, 1)
        
        

        
suite = unittest.defaultTestLoader.loadTestsFromTestCase(NativeObjectTest)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
