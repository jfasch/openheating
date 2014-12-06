class Source:
    def __init__(self):
        self.__requesters = set()
    def request(self, sink):
        self.__requesters.add(sink)
    def release(self, sink):
        self.__requesters.remove(sink)
    def requesters(self):
        return self.__requesters
