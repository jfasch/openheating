from ..logic.switch import Switch

class TestSwitch(Switch):
    def __init__(self, name, initial_state, output=None):
        self.__name = name
        self.__output = output
        self.set_state(initial_state)

    def set_state(self, state):
        assert type(state) is bool, type(state)
        self.__do_output(state)
        self.__state = state
    def get_state(self):
        return self.__state

    def __do_output(self, state):
        if self.__output is None:
            return
        if state:
            msg = ": closing"
        else:
            msg = ": opening"
        print(self.__name + msg, file=self.__output)
