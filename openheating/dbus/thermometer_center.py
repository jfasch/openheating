from . import names
from .thermometer import Thermometer_Client
from .temperature_history import TemperatureHistory_Client
from ..error import HeatingError


class ThermometerCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/',
            iface=names.IFACE.THERMOMETER_CENTER)

    def all_names(self):
        return self.__iface.all_names()

    def get_thermometer(self, name):
        return Thermometer_Client(
            proxy=self.__get_object_iface(
                busname=names.BUS.THERMOMETER_SERVICE,
                path='/thermometers/'+name, 
                iface=names.IFACE.THERMOMETER))

    def get_history(self, name):
        return TemperatureHistory_Client(
            proxy=self.__get_object_iface(
                busname=names.BUS.THERMOMETER_SERVICE,
                path='/history/'+name, 
                iface=names.IFACE.TEMPERATURE_HISTORY))

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]
    

class ThermometerCenter_Server:
    dbus = """
    <node>
      <interface name='{thermometer_center_iface}'>
        <method name='all_names'>
          <arg type='as' name='response' direction='out'/>
        </method>
      </interface>
    </node>
    """.format(thermometer_center_iface=names.IFACE.THERMOMETER_CENTER)

    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def all_names(self):
        return self.__thermometers.keys()
