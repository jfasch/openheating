from ..control.switch import Switch

class TestSwitch(Switch):
    def __init__(self, on):
        assert type(on) is bool        
        self.__on = on
    def on(self):
        self.__on = True
    def off(self):
        self.__on = False
    def is_on(self):
        return self.__on
