from ..switch import Switch

class TestSwitch(Switch):
    def __init__(self, initial_state, output=None):
        self.__output = output
        self.set_state(initial_state)

    def set_state(self, state):
        assert state in (self.OPEN, self.CLOSED)
        self.__do_output(state)
        self.__state = state
    def get_state(self):
        return self.__state

    def __do_output(self, state):
        if self.__output is None:
            return
        if state == self.OPEN:
            print("open", file=self.__output)
            return
        if state == self.CLOSED:
            print("closed", file=self.__output)
            return
        assert False, state
