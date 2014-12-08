import os.path

_root = '/sys/class/gpio'

IN, OUT = 0, 1

class SysFS_GPIO_Manager:
    def __init__(self):
        pass
    
    def create(self, number):
        path = '%s/gpio%d' % (_root, number)
        if not os.path.exists(path):
            open(_root + '/export', 'wb').write(str(number)+'\n')
        return _SysFS_GPIO(number)
        
class _SysFS_GPIO:
    def __init__(self, number):
        self.__number = number
        self.__value = '%s/gpio%d/value' % (_root, number)
        self.__direction = '%s/gpio%d/direction' % (_root, number)
    def __del__(self):
        open(_root + '/unexport', 'wb').write(str(number)+'\n')
    def set_direction(self, inout):
        assert inout in (IN, OUT)
        open(self.__direction, 'wb').write(inout == IN and 'in' or 'out')
    def get_direction(self):
        return open(self.__direction, 'rb').read() == 'in\n' and IN or OUT
    def set_value(self, value):
        open(self.__value, 'wb').write(str(value)+'\n')
    def get_value(self):
        open(self.__value, 'rb').read() == '0\n' and 0 or 1
