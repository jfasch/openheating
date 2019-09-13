from openheating.dbus import names

import ravel


class ThermometerHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def decision_history(self):
        return self.__proxy.decision_history()[0]

    def hour_history(self):
        return self.__proxy.hour_history()[0]

    def day_history(self):
        return self.__proxy.day_history()[0]

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER_HISTORY)
class ThermometerHistory_Server:
    def __init__(self, decision_history, hour_history, day_history):
        self.__decision_history = decision_history
        self.__hour_history = hour_history
        self.__day_history = day_history

    @ravel.method(
        name = 'decision_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    def decision_history(self):
        return (list(self.__decision_history),)

    @ravel.method(
        name = 'hour_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    def hour_history(self):
        return (list(self.__hour_history),)

    @ravel.method(
        name = 'day_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    def day_history(self):
        return (list(self.__day_history),)

