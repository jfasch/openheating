class TestPoller:
    def __init__(self, pollees):
        self.__pollees = pollees
    def poll(self):
        for p in self.__pollees:
            p.poll()
