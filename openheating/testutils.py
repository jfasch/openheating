import os, shutil, unittest

class PersistentTestCase(unittest.TestCase):

    sequential_number = 0
    
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        pass

    def rootpath(self):
        return self.__my_rootpath

    def setUp(self):
        self.__my_rootpath = '/tmp/openheating.'+str(os.getpid())+'.'+ str(PersistentTestCase.sequential_number)+'.'+ self.__class__.__name__
        os.mkdir(self.__my_rootpath)
        PersistentTestCase.sequential_number += 1
        pass
    
    def tearDown(self):
        dir = os.sep.join(self.__my_rootpath)
        if os.path.isdir(dir):
            if os.environ.get('KEEP_PERSISTENT_TEST') is None:
                shutil.rmtree(dir)
                pass
            pass
        pass

    pass
