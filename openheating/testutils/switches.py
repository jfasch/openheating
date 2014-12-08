from ..switch import Switch

class TestSwitch(Switch):
    def __init__(self, on):
        assert type(on) is bool        
        self.__state = on
    def set_state(self, value):
        self.__state = value
    def is_on(self):
        return self.__state
