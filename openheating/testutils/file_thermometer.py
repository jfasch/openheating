from ..thermometer import Thermometer
from ..error import HeatingError

class FileThermometer(Thermometer):
    def __init__(self, path):
        self.__path = path
    def temperature(self):
        try:
            return float(open(self.__path).read())
        except Exception as e:
            raise HeatingError('File thermometer "%s": cannot get temperature: %s' % (self.__path, str(e)),
                               permanent=True)
