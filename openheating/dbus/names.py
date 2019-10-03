DOMAIN = 'org.openheating'

class BUS:
    THERMOMETER_SERVICE = DOMAIN + '.ThermometerService'
    ERROR_SERVICE = DOMAIN + '.ErrorService'
    SWITCH_SERVICE = DOMAIN + '.SwitchService'

class IFACE:
    THERMOMETER = DOMAIN + '.Thermometer'
    TEMPERATURE_HISTORY = DOMAIN + '.TemperatureHistory'
    SWITCH = DOMAIN + '.Switch'
    THERMOMETER_CENTER = DOMAIN + '.ThermometerCenter'
    SWITCH_CENTER = DOMAIN + '.SwitchCenter'

class EXCEPTION:
    HEATINGERROR = DOMAIN + '.HeatingError'
