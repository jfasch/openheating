from . import names
from . import ifaces


class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def decision_history(self):
        return self.__proxy.decision_history()[0]

    def hour_history(self):
        return self.__proxy.hour_history()[0]

    def day_history(self):
        return self.__proxy.day_history()[0]


@ifaces.TEMPERATURE_HISTORY.iface
class TemperatureHistory_Server:
    def __init__(self, decision_history, hour_history, day_history):
        self.__decision_history = decision_history
        self.__hour_history = hour_history
        self.__day_history = day_history

    @ifaces.TEMPERATURE_HISTORY.decision_history
    def decision_history(self):
        return (list(self.__decision_history),)

    @ifaces.TEMPERATURE_HISTORY.hour_history
    def hour_history(self):
        return (list(self.__hour_history),)

    @ifaces.TEMPERATURE_HISTORY.day_history
    def day_history(self):
        return (list(self.__day_history),)
