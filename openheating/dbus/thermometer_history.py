from openheating.dbus import names

import ravel


class ThermometerHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def all(self):
        return self.__proxy.all()[0]

    def cutout(self, youngest, oldest):
        return self.__proxy.cutout(youngest, oldest)[0]

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER_HISTORY)
class ThermometerHistory_Server:
    def __init__(self, history):
        self.__history = history

    @ravel.method(
        name = 'all',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    def all(self):
        return (self.__history.all(),)

    @ravel.method(
        name = 'cutout',
        in_signature = 'tt', # uint64:youngest,uint64:oldest
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    def cutout(self, youngest, oldest):
        return (self.__history.cutout(youngest=youngest, oldest=oldest),)

