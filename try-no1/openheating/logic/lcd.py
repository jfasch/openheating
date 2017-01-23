from .thinker import LeafThinker

from .thermometer_center import ThermometerCenterThermometer
from ..hardware.hd44780 import HD44780_LCD
from ..base.error import HeatingError

from datetime import datetime


class LCD(LeafThinker):
    def __init__(self,
                 name,
                 thermometer_center,

                 boiler_top,
                 boiler_middle,
                 boiler_bottom,
                 hk_vl,
                 boiler_vl,
                 ofen_vl,
                 ofen,
                 oel_puffer,
                 essraum,

                 simulation=False):

        LeafThinker.__init__(self, name)

        self.__simulation = simulation
        if not self.__simulation:
            self.__lcd = HD44780_LCD(rs=27, en=22, d4=25, d5=24, d6=23, d7=18, cols=20, lines=4)

        self.__boiler_top = ThermometerCenterThermometer(center=thermometer_center, name=boiler_top)
        self.__boiler_middle = ThermometerCenterThermometer(center=thermometer_center, name=boiler_middle)
        self.__boiler_bottom = ThermometerCenterThermometer(center=thermometer_center, name=boiler_bottom)
        self.__hk_vl = ThermometerCenterThermometer(center=thermometer_center, name=hk_vl)
        self.__boiler_vl = ThermometerCenterThermometer(center=thermometer_center, name=boiler_vl)
        self.__ofen_vl = ThermometerCenterThermometer(center=thermometer_center, name=ofen_vl)
        self.__ofen = ThermometerCenterThermometer(center=thermometer_center, name=ofen)
        self.__oel_puffer = ThermometerCenterThermometer(center=thermometer_center, name=oel_puffer)
        self.__essraum = ThermometerCenterThermometer(center=thermometer_center, name=essraum)
    
    def think(self):
        temps = {
            'now': str(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')),
            'essraum': self.__get_temperature(self.__essraum, 1),
            'boiler-top': self.__get_temperature(self.__boiler_top, 0),
            'boiler-middle': self.__get_temperature(self.__boiler_middle, 0),
            'boiler-bottom': self.__get_temperature(self.__boiler_bottom, 0),
            'hk-vl': self.__get_temperature(self.__hk_vl, 1),
            'boiler-vl': self.__get_temperature(self.__boiler_vl, 1),
            'ofen-vl': self.__get_temperature(self.__ofen_vl, 1),
            'ofen': self.__get_temperature(self.__ofen, 1),
            'oel-puffer': self.__get_temperature(self.__oel_puffer, 1),
            }
        msg = \
            ('%(now)s\n' + \
             'E:%(essraum)s    B:%(boiler-top)s/%(boiler-middle)s/%(boiler-bottom)s\n' + \
             'O:%(oel-puffer)s   H:%(ofen)s/%(ofen-vl)s\n' + \
             'HK:%(hk-vl)s      WW:%(boiler-vl)s'
             ) % temps
    
        if self.__simulation:
            print(msg+'\n--')
        else:
            self.__lcd.clear()
            self.__lcd.message(msg)

        return []
        
    @staticmethod
    def __get_temperature(thermometer, places):
        try:
            return ('%.'+str(places)+'f') % thermometer.temperature()
        except HeatingError:
            return 'ERR!'
        
