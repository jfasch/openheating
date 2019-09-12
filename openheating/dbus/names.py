DOMAIN = 'org.openheating'

class BUS:
    THERMOMETER_SERVICE = DOMAIN + '.ThermometerService'
    SWITCH_SERVICE = DOMAIN + '.SwitchService'

class IFACE:
    THERMOMETER = DOMAIN + '.Thermometer'
    THERMOMETER_HISTORY = DOMAIN + '.ThermometerHistory'
    SWITCH = DOMAIN + '.Switch'
    THERMOMETER_CENTER = DOMAIN + '.ThermometerCenter'
    SWITCH_CENTER = DOMAIN + '.SwitchCenter'

class DATA:
    ERROR = DOMAIN + '.HeatingError'
