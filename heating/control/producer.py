class Producer:
    def __init__(self, backend):
        self.__backend = backend
        self.__acquirers = set()
        
    def temperature(self):
        return self.__backend.temperature()

    def acquire(self, name):
        num_before = len(self.__acquirers)
        self.__acquirers.add(name)
        if num_before == 0 and len(self.__acquirers) > 0:
            self.__backend.start_producing()

    def release(self, name):
        num_before = len(self.__acquirers)
        self.__acquirers.discard(name)
        if num_before > 0 and len(self.__acquirers) == 0:
            self.__backend.stop_producing()

    def is_acquired(self):
        return len(self.__acquirers) > 0

    def acquirers(self):
        ''' For testing only, irrelevant in real life '''
        return self.__acquirers
        
    def needs_cooling(self):
        return self.__backend.needs_cooling()
        
    
