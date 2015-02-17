from .source import Source
from .thinking import Thinker, ThinkingSwitch
from .hysteresis import Hysteresis

class OilCombo(Source, Thinker):
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
                 heating_level,
                 minimum_temperature_hysteresis,
                 max_produced_temperature):
        assert isinstance(minimum_temperature_hysteresis, Hysteresis)
        assert type(max_produced_temperature) in (int, float)

        Source.__init__(self, name=name, max_produced_temperature=max_produced_temperature)
        
        self.__burn_switch = ThinkingSwitch(burn_switch)
        self.__thermometer = thermometer
        self.__heating_level = heating_level
        self.__minimum_temperature_hysteresis = minimum_temperature_hysteresis

    def temperature(self):
        return self.__thermometer.temperature()

    def think(self):
        temperature = self.__thermometer.temperature()

        if (self.num_requesters() > 0 and self.__heating_level.below(temperature)) \
           or self.__minimum_temperature_hysteresis.below(temperature):
            return self.__burn_switch.set(True)

        if (self.num_requesters() == 0 or self.__heating_level.above(temperature)) \
           and self.__minimum_temperature_hysteresis.above(temperature):
            return self.__burn_switch.set(False)

        return 0
        
    def sync(self):
        self.__burn_switch.sync()
