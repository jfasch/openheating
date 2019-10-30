from . import dbusutil
from . import node
from .thermometer import Thermometer_Client, TemperatureHistory_Client
from ..error import HeatingError


class ThermometerCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=dbusutil.THERMOMETERS_BUSNAME,
            path='/',
            iface=dbusutil.THERMOMETERCENTER_IFACENAME)

    def all_names(self):
        return self.__iface.all_names()


    def get_thermometer(self, name):
        return Thermometer_Client(
            proxy=self.__get_object_iface(
                busname=dbusutil.THERMOMETERS_BUSNAME,
                path='/thermometers/'+name, 
                iface=dbusutil.THERMOMETER_IFACENAME))

    def get_history(self, name):
        return TemperatureHistory_Client(
            proxy=self.__get_object_iface(
                busname=dbusutil.THERMOMETERS_BUSNAME,
                path='/thermometers/'+name, 
                iface=dbusutil.TEMPERATUREHISTORY_IFACENAME))

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]
    

@node.Definition(interfaces=(dbusutil.THERMOMETERCENTER_IFACEXML,))
class ThermometerCenter_Server:
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def all_names(self):
        return self.__thermometers.keys()
