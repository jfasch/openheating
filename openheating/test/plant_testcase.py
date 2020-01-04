from . import testutils

from ..base.error import HeatingError
from ..dbus import names

import pydbus

import tempfile
import subprocess
import sys
import unittest


class PlantTestCase(unittest.TestCase):
    '''TestCase derivative which is good at managing dbus services as
    subprocesses.

    If failure is detected (see the intercept_failure() decorator),
    then at tearDown the stderr output of each service is printed.

    '''

    @staticmethod
    def intercept_failure(testmethod):
        '''test method decorator to intercept test case failures (these are
        hard to come by otherwise)

        '''
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return testmethod(*args, **kwargs)
            except:
                self.__failure = True
                raise
        return wrapper

    def setUp(self):
        self.__is_failure = False
        self.__plant = None
    def tearDown(self):
        if self.__plant:
            self.__plant.shutdown(self.__is_failure)

    def start_plant(self, plant):
        self.__plant = plant
        self.__plant.startup()
