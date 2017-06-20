from . import names

import pydbus


class Thermometer:
    '''
    <node>
      <interface name='org.openheating.Thermometer'>
        <method name='get_temperature'>
          <arg type='d' name='temperature' direction='out'/>
        </method>
      </interface>
    </node>
    '''

    def __init__(self, thermometer):
        self.__thermometer = thermometer

    def get_temperature(self):
        return self.__thermometer.get_temperature()

