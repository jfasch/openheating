from ..switch import Switch
from ..error import HeatingError

import re


re_on = re.compile('\s*on\s*$')
re_off = re.compile('\s*off\s*$')

class FileSwitch(Switch):
    def __init__(self, path):
        self.__path = path

    def set_state(self, value):
        try:
            open(self.__path, 'w').write(value and 'on\n' or 'off\n')
        except Exception as e:
            raise HeatingError('File switch "%s": cannot set state: %s' % (self.__path, str(e)),
                               permanent=True)

    def get_state(self):
        try:
            content = open(self.__path).read()
        except Exception as e:
            raise HeatingError('File switch "%s": cannot get state: %s' % (self.__path, str(e)),
                               permanent=True)
            
        match = re_on.search(content)
        if match:
            return True
        match = re_off.search(content)
        if match:
            return False
        # neither on nor off? don't care for the time being - see
        # where this leads us
        assert False, content
