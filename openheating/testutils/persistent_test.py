import os, shutil, unittest


class PersistentTestCase(unittest.TestCase):

    sequential_number = 0
    
    def rootpath(self):
        return self.__rootpath

    def setUp(self):
        self.__rootpath = '/tmp/openheating.'+str(os.getpid())+'.'+ str(PersistentTestCase.sequential_number)+'.'+ self.__class__.__name__
        os.mkdir(self.__rootpath)
        self.sequential_number += 1
    
    def tearDown(self):
        if os.environ.get('KEEP_PERSISTENT_TEST') is None:
            shutil.rmtree(self.__rootpath)
