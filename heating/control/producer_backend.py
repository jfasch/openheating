from abc import ABCMeta, abstractmethod

class ProducerBackend(metaclass=ABCMeta):
    @abstractmethod
    def temperature(self):
        assert False, 'abstract'
        return 25.4

    @abstractmethod
    def start_producing(self):
        ''' Called when temperature is needed but not there '''
        assert False, 'abstract'

    @abstractmethod
    def stop_producing(self):
        ''' Called when temperature is not needed anymore '''
        assert False, 'abstract'
