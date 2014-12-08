import os.path

_root = '/sys/class/gpio'

IN, OUT = 0, 1

class SysFS_GPIO_Manager:
    def __init__(self):
        pass
    
    def create(self, number):
        path = '%s/gpio%d' % (_root, number)
        if not os.path.exists(path):
            open(_root + '/export', 'w').write(str(number)+'\n')
        return _SysFS_GPIO(number)
        
class _SysFS_GPIO:
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
        open(self.__value, 'w').write(str(value)+'\n')
    def get_value(self):
        return open(self.__value, 'r').read() == '0\n' and 0 or 1
