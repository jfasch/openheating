from .thermometer import Thermometer


class FixedThermometer(Thermometer):
    def __init__(self, name, description, temperature):
        super().__init__(name, description)
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature
