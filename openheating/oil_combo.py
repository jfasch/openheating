class OilCombo:
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
                 burn_switch,
                 thermometer,
                 max_temperature):
        self.__burn_switch = burn_switch
        self.__thermometer = thermometer
        self.__max_temperature = max_temperature

    def temperature(self):
        return self.__thermometer.temperature()

    def request(self):
        '''Called by a dedicated source when a sink wants heat.'''

        buffer_temperature = self.__thermometer.temperature()
        if self.__max_temperature.above(buffer_temperature):
            self.__burn_switch.do_open()
        elif self.__max_temperature.below(buffer_temperature):
            self.__burn_switch.do_close()
        else:
            # leave as-is
            pass

    def release(self):
        self.__burn_switch.do_open()
