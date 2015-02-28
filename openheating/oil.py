from .source import DirectSource
from .hysteresis import Hysteresis

import logging


class OilCombo(DirectSource):
    '''Burner with Riello schematics (simple thing I think), together with
    a thermometer to measure water storage temperature.

    Simple on/off on request()/release(), though there's more: 

    * http://www.mikrocontroller.net/topic/141478: minimum of 35deg
      during heating.

    * http://forum.electronicwerkstatt.de/phpBB/Bauteile/anschlussbelegung_oelbrenner-t91974f30_bs0.html
      http://www.kolboske.de/cms/mat/hz/oel_brenner_sammelsorium.pdf
      http://www.bosy-online.de/Brenneranschluss.htm

    * http://www.mikrocontroller.net/topic/37080#273786: hysteresis
      65-75deg

    Kesseldatenblatt wegen Idealtemperatur?

    Ruecklauf ueber Boiler zum Heizen von dem!?

    "Wieland/Euro-Stecker"

    '''
    def __init__(self,
                 name,
                 burn_switch,
                 thermometer,
                 heating_range,
                 minimum_temperature_range,
                 max_produced_temperature):
        assert isinstance(minimum_temperature_range, Hysteresis)
        assert type(max_produced_temperature) in (int, float)
        assert minimum_temperature_range.high() < heating_range.high()

        DirectSource.__init__(self, name=name, max_produced_temperature=max_produced_temperature)
        
        self.__burn_switch = burn_switch
        self.__thermometer = thermometer
        self.__heating_range = heating_range
        self.__minimum_temperature_range = minimum_temperature_range

    def temperature(self):
        return self.__thermometer.temperature()

    def start_thinking(self):
        super().start_thinking()
        self.__temperature = self.__thermometer.temperature()

    def stop_thinking(self):
        if self.__heating_range.above(self.__temperature):
            self.__debug('hot enough, off: temperature=%f,heat/hi=%f' % (self.__temperature, self.__heating_range.high()))
            self.__burn_switch.do_open()
        elif self.__heating_range.below(self.__temperature):
            if self.num_requests() > 0:
                self.__debug('not hot enough, on: temperature=%f,heat/lo=%f,requests=%s' % \
                             (self.__temperature, self.__minimum_temperature_range.low(), self.print_requests()))
                self.__burn_switch.do_close()
            elif self.__minimum_temperature_range.below(self.__temperature):
                self.__debug('anti frost, on: temperature=%f,min/lo=%f' % \
                             (self.__temperature, self.__minimum_temperature_range.low()))
                self.__burn_switch.do_close()
            elif self.__minimum_temperature_range.above(self.__temperature):
                self.__debug('anti frost done, off: temperature=%f,min/hi=%f' % \
                             (self.__temperature, self.__minimum_temperature_range.high()))
                self.__burn_switch.do_open()
            else:
                self.__debug('anti frost in range, leaving as-is')
                pass
            pass

        del self.__temperature
        super().stop_thinking()

    def think(self):
        return 0

    def __debug(self, msg):
        logging.debug(self.name()+': '+msg)
