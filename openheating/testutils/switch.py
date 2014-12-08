from ..switch import Switch

class TestSwitch(Switch):
    def __init__(self, state):
        self.set_state(state)
    def set_state(self, state):
        assert state in (self.OPEN, self.CLOSED)
        self.__state = state
    def get_state(self):
        return self.__state
