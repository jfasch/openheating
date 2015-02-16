from .source import Source
from .thinking import Thinker

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
                 enable_switch,
                 burn_switch,
                 thermometer):
        Source.__init__(self, name=name)
        
        self.__enable_switch = enable_switch
        self.__burn_switch = burn_switch
        self.__thermometer = thermometer

    def temperature(self):
        return self.__thermometer.temperature()

    def enable(self):
        '''Close the "enable" switch'''
        self.__enable_switch.do_close()
    def disable(self):
        '''Open the "enable" switch'''
        self.__enable_switch.do_open()

    def think(self):
        return 0
    def sync(self):
        pass

    def do_request(self):
        self.__burn_switch.do_close()

    def do_release(self):
        self.__burn_switch.do_open()
        
