class Transport:
    (ON, OFF) = xrange(2)
    
    def __init__(self,
                 consumer_temperature_wanted,
                 consumer_thermometer,
                 producer_thermometer,
                 hardware_device):
        self.__consumer_temperature_wanted = consumer_temperature_wanted
        self.__consumer_thermometer = consumer_thermometer
        self.__producer_thermometer = producer_thermometer
        self.__hardware_device = hardware_device
        self.__state = self.OFF

    def check(self):
        while True:
            if self.__consumer_thermometer.get_temperature() < self.__consumer_temperature_wanted:
                if self.__state == self.OFF:
                    self.__hardware_device.on()
                    self.__state = self.ON
            
