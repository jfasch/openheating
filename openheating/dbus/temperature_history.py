from . import names
from . import ifaces

from .. import timeutil


class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def distill(self, granularity, duration):
        return self.__proxy.distill(
            timeutil.delta2unix(granularity), 
            timeutil.delta2unix(duration))[0]


@ifaces.TEMPERATURE_HISTORY.iface
class TemperatureHistory_Server:
    def __init__(self, history):
        self.__history = history

    @ifaces.TEMPERATURE_HISTORY.distill
    def distill(self, granularity, duration):
        distilled = self.__history.distill(granularity=granularity, duration=duration)
        return (list(distilled),)
