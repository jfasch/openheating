DOMAIN = 'org.openheating'

class BUS:
    THERMOMETER_SERVICE = DOMAIN + '.ThermometerService'
    SWITCH_SERVICE = DOMAIN + '.SwitchService'

class IFACE:
    THERMOMETER = DOMAIN + '.Thermometer'
    SWITCH = DOMAIN + '.Switch'
    THERMOMETER_SERVICE = DOMAIN + '.ThermometerService'
    SWITCH_SERVICE = DOMAIN + '.SwitchService'

class DATA:
    ERROR = DOMAIN + '.HeatingError'
