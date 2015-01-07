from ..error import HeatingError

import os.path
import os
import time

_root = '/sys/class/gpio'

IN, OUT = 0, 1

def create(number):
    path = '%s/gpio%d' % (_root, number)
    if not os.path.exists(path):
        open(_root + '/export', 'w').write(str(number)+'\n')

    # wait for files to appear before using it any further. this
    # happened to be a problem on Raspi's 3.12.28+ #709, at least,
    # where it said EACCESS on the 'direction' file when using it "too
    # early" after export.
    direction = path + '/direction'
    num_tries = 100
    while not os.access(direction, os.R_OK|os.W_OK):
        time.sleep(0.05)
        num_tries -= 1
        if num_tries == 0:
            raise HeatingError(direction + " didn't become rw-able after 100 tries")

    return _SysFS_GPIO(number)

class _SysFS_GPIO:

    __HI = '1\n'
    __LO = '0\n'
    
    def __init__(self, number):
        self.__number = number
        self.__value = '%s/gpio%d/value' % (_root, number)
        self.__direction = '%s/gpio%d/direction' % (_root, number)
    def __del__(self):
        open(_root + '/unexport', 'w').write(str(self.__number)+'\n')
    def set_direction(self, inout):
        assert inout in (IN, OUT)
        open(self.__direction, 'w').write(inout == IN and 'in' or 'out')
    def get_direction(self):
        return open(self.__direction, 'r').read() == 'in\n' and IN or OUT
    def set_value(self, value):
        f = open(self.__value, 'w')
        if value:
            f.write(self.__HI)
        else:
            f.write(self.__LO)
    def get_value(self):
        f = open(self.__value, 'r')
        content = f.read()
        f.close()

        if content == self.__LO:
            return 0
        elif content == self.__HI:
            return 1
        assert False, content
