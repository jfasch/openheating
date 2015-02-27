class TemperatureRequests:
    def __init__(self):
        self.__requests = {}

    def add(self, sink, temperature):
        self.__requests[sink] = temperature

    def clear(self):
        self.__requests.clear()

    def num_requests(self):
        return len(self.__requests)

    def is_member(self, sink):
        return self.__requests.get(sink) is not None

    def __str__(self):
        return ','.join(['%s(%f)' % (sink.name(), temperature) for sink, temperature in self.__requests.items()])
