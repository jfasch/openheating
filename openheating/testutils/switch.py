from ..switch import Switch

class TestSwitch(Switch):
    def __init__(self, initial_state):
        self.set_state(initial_state)
    def set_state(self, state):
        assert state in (self.OPEN, self.CLOSED)
        self.__state = state
    def get_state(self):
        return self.__state
