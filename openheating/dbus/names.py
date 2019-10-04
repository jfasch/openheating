DOMAIN = 'org.openheating'

class BUS:
    THERMOMETERS = DOMAIN + '.Thermometers'
    ERRORS = DOMAIN + '.Errors'
    SWITCHES = DOMAIN + '.Switches'

class IFACE:
    THERMOMETER = DOMAIN + '.Thermometer'
    TEMPERATURE_HISTORY = DOMAIN + '.TemperatureHistory'
    SWITCH = DOMAIN + '.Switch'
    THERMOMETER_CENTER = DOMAIN + '.ThermometerCenter'
    SWITCH_CENTER = DOMAIN + '.SwitchCenter'

class EXCEPTION:
    HEATINGERROR = DOMAIN + '.HeatingError'
