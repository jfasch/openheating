from . import names

from .. import timeutil


class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def distill(self, granularity, duration):
        return self.__proxy.distill(
            timeutil.delta2unix(granularity), 
            timeutil.delta2unix(duration))


class TemperatureHistory_Server:
    dbus = """
    <node>
      <interface name='{thermometer_history_iface}'>
        <method name='distill'>
          <arg type='t' name='granularity' direction='in'/>
          <arg type='t' name='duration' direction='in'/>
          <arg type='a(td)' name='response' direction='out'/>
        </method>
      </interface>
    </node>
    """.format(thermometer_history_iface=names.IFACE.TEMPERATURE_HISTORY)

    def __init__(self, history):
        self.__history = history

    def distill(self, granularity, duration):
        distilled = self.__history.distill(granularity=granularity, duration=duration)
        return distilled
