from abc import ABCMeta, abstractmethod

class Producer(metaclass=ABCMeta):
    @abstractmethod
    def temperature(self):
        assert False, 'abstract'
        return 25.4
    @abstractmethod
    def acquire(self):
        ''' Called when temperature is needed but not there '''
        assert False, 'abstract'
    @abstractmethod
    def release(self):
        ''' Called when temperature is not needed anymore '''
        assert False, 'abstract'
    pass
