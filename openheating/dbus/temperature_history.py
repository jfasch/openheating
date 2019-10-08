from . import dbusutil

from .. import timeutil


class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def distill(self, granularity, duration):
        return self.__proxy.distill(
            timeutil.delta2unix(granularity), 
            timeutil.delta2unix(duration))


class TemperatureHistory_Server:
    def __init__(self, history):
        self.__history = history

    def distill(self, granularity, duration):
        distilled = self.__history.distill(granularity=granularity, duration=duration)
        return distilled

dbusutil.define_node(klass=TemperatureHistory_Server, interfaces=(dbusutil.TEMPERATUREHISTORY_IFACEXML,))
