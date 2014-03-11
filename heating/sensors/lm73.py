class LM73:
    RESOLUTIONS = (RES0_25, RES0_125, RES0_0625, RES0_03125) = (0b00, 0b01, 0b10, 0b11)
    
    def __init__(self, simulated_temperature=None, simulated_resolution=None):
        assert simulated_temperature is None and simulated_resolution is None \
            or simulated_temperature is not None and simulated_resolution is not None
        
        if simulated_temperature is None:
            self.__simulated_temperature = None
        else:
            self.__simulated_temperature = _to_twobyte_temp(simulated_temperature,
                                                            simulated_resolution)
            pass

        self.__resolution = simulated_resolution
        pass

    def get_temperature(self):
        assert self.__simulated_temperature is not None, 'implement: fetch temperature'
        return _from_twobyte_temp(self.__simulated_temperature, self.__resolution)

    def set_resolution(self, r):
        assert r in self.RESOLUTIONS
        assert self.__simulated_temperature, 'implement: send resolution to the device'
        self.__resolution = r
        pass

    def get_resolution(self):
        if self.__resolution is None:
            assert self.__simulated_temperature, 'implement: get resolution from the device (really, should we)'
            pass
        return self.__resolution

    pass

def _to_twobyte_temp(t, r):
    return 0

def _from_twobyte_temp(t, r):
    return 0
