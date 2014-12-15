from .source import Source

class OilCombo(Source):
    '''Burner with Riello schematics (simple thing I think), together with
    a thermometer to measure water storage temperature.

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

    def do_request(self):
        self.__burn_switch.do_close()

    def do_release(self):
        self.__burn_switch.do_open()
        
