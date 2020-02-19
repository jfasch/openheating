DOMAIN = 'org.openheating'

HEATINGERROR = DOMAIN + '.HeatingError'

class Bus:
    MAIN = DOMAIN + '.Main'
    THERMOMETERS = DOMAIN + '.Thermometers'
    SWITCHES = DOMAIN + '.Switches'
    CIRCUITS = DOMAIN + '.Circuits'
    ERRORS = DOMAIN + '.Errors'
    EXCEPTIONTESTER = DOMAIN + '.ExceptionTester'
    MANAGEDOBJECTTESTER = DOMAIN + '.ManagedObjectTester'
    POLLWITNESS = DOMAIN + '.PollWitness'
    CRASHTESTDUMMY = DOMAIN + '.CrashTestDummy'

class ThermometerPaths:
    CENTER = '/'
    
    @staticmethod
    def THERMOMETER(name):
        return '/thermometers/'+name
