from .source import DirectSource
from .hysteresis import Hysteresis

from ..base import logger


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

    def init_thinking_local(self):
        super().init_thinking_local()
        self.__temperature = self.__thermometer.temperature()
        self.__switch_state = None

    def finish_thinking_local(self):
        super().finish_thinking_local()
        if self.__switch_state is not None:
            self.__burn_switch.set_state(self.__switch_state)
        del self.__temperature
        del self.__switch_state

    def think(self):
        if self.__heating_range.above(self.__temperature):
            msg = 'hot enough, off: temperature=%.1f,heat/hi=%.1f' % (self.__temperature, self.__heating_range.high())
            self.__debug(msg)
            return self.__think_set_switch_state(False, msg)
        if self.__heating_range.below(self.__temperature):
            if self.num_requests() > 0:
                msg = 'not hot enough, on: temperature=%.1f,heat/lo=%.1f,requests=%s' % \
                      (self.__temperature, self.__minimum_temperature_range.low(), self.print_requests())
                self.__debug(msg)
                return self.__think_set_switch_state(True, msg)
            if self.__minimum_temperature_range.below(self.__temperature):
                msg = 'anti frost, on: temperature=%.1f,min/lo=%.1f' % \
                      (self.__temperature, self.__minimum_temperature_range.low())
                self.__debug(msg)
                return self.__think_set_switch_state(True, msg)
            if self.__minimum_temperature_range.above(self.__temperature):
                msg = 'anti frost done, off: temperature=%.1f,min/hi=%.1f' % \
                      (self.__temperature, self.__minimum_temperature_range.high())
                self.__debug(msg)
                return self.__think_set_switch_state(False, msg)
        return []

    def __debug(self, msg):
        logger.debug(self.name()+': '+msg)

    def __think_set_switch_state(self, state, msg):
        if self.__switch_state == state:
            return []
        else:
            self.__switch_state = state
            return [(self.name(), msg)]
