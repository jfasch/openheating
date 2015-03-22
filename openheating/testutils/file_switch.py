from ..switch import Switch

import re

re_on = re.compile('\s*on\s*$')
re_off = re.compile('\s*off\s*$')

class FileSwitch(Switch):
    def __init__(self, path):
        self.__path = path
    def set_state(self, value):
        open(self.__path, 'w').write(value and 'on\n' or 'off\n')
    def get_state(self):
        content = open(self.__path).read()
        match = re_on.search(content)
        if match:
            return True
        match = re_off.search(content)
        if match:
            return False
        # don't care for the time being - see where this leads us
        assert False, content
