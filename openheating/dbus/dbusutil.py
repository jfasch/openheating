from ..error import HeatingError

from pydbus import SystemBus, SessionBus

import json
import signal


def argparse_add_bus(parser):
    '''add --session|--system options to commandline parsing'''

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus_from_argparse(args):
    '''given --session|--system is in argparse, connect to the respective
    bus, and return the bus object'''

    return args.session and SessionBus() or SystemBus()

def graceful_termination(loop):
    '''install the appropriate signal handler, and take care to terminate
    the eventloop gracefully'''

    def quit(signal, frame):
        loop.quit()
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    signal.signal(signal.SIGQUIT, quit)



# centrally defined names, to ease modifications
DOMAIN = 'org.openheating'

# bus names
THERMOMETERS_BUSNAME = DOMAIN + '.Thermometers'
ERRORS_BUSNAME = DOMAIN + '.Errors'
EXCEPTIONTESTER_BUSNAME = DOMAIN + '.ExceptionTester'

# interface names and XML fragments
THERMOMETER_IFACENAME = DOMAIN + '.Thermometer'
THERMOMETER_IFACEXML = '''
<interface name='{name}'>
  <method name='get_name'>
    <arg type='s' name='response' direction='out'/>
  </method>
  <method name='get_description'>
    <arg type='s' name='response' direction='out'/>
  </method>
  <method name='get_temperature'>
    <arg type='d' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=THERMOMETER_IFACENAME)

ERROREMITTER_IFACENAME = DOMAIN + '.ErrorEmitter'
ERROREMITTER_IFACEXML = '''
<interface name='{name}'>
  <signal name="error">
    <arg type="s" name="what" direction="out"/>
  </signal>
</interface>
'''.format(name=ERROREMITTER_IFACENAME)

TEMPERATUREHISTORY_IFACENAME = DOMAIN + '.TemperatureHistory'
TEMPERATUREHISTORY_IFACEXML = '''
<interface name='{name}'>
  <method name='distill'>
    <arg type='t' name='granularity' direction='in'/>
    <arg type='t' name='duration' direction='in'/>
    <arg type='a(td)' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=TEMPERATUREHISTORY_IFACENAME)

THERMOMETERCENTER_IFACENAME = DOMAIN + '.ThermometerCenter'
THERMOMETERCENTER_IFACEXML = '''
<interface name='{name}'>
  <method name='all_names'>
    <arg type='as' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=THERMOMETERCENTER_IFACENAME)

EXCEPTIONTESTER_IFACENAME = DOMAIN + '.ExceptionTester'
EXCEPTIONTESTER_IFACEXML = '''
<interface name='{name}'>
  <method name='raise_default_HeatingError'>
    <arg type='s' name='msg' direction='in'/>
  </method>
  <method name='raise_derived_default_HeatingError'>
    <arg type='s' name='msg' direction='in'/>
  </method>
</interface>
'''.format(name=EXCEPTIONTESTER_IFACENAME)


HEATINGERROR_NAME = DOMAIN + '.HeatingError'

class DBusHeatingError(HeatingError):
    '''Used to pass HeatingError exceptions across the bus.

    Use @unify_error to decorate interface method implementations,
    converting native HeatingError exceptions into a DBusHeatingError.

    DBusHeatingError then collaborates with pydbus and brings the
    error across the bus: 

    * on occurence (a server method throws), pydbus calls str() on it
      to build the dbus ERROR argument (dbus string).

    * at the client, when that sees a dbus ERROR, it call the
      registered class ctor on the (json) string, converting it back
      to a native DBusHeatingError. which is then thrown at the user.

    '''
    def __init__(self, details):
        if type(details) is str:
            # assume it came across the bus, so it must be json.
            details = json.loads(details)
        super().__init__(details=details)

    def __str__(self):
        '''pydbus calls str() on mapped exceptions to create the dbus ERROR
        argument. we want our heating errors to travel as json, and
        that's what we do in __str__()

        '''
        return json.dumps(self.details)

def unify_error(fun):
    '''Used as a decorator for callables that raise derived HeatingError
    instances. (Generally, dbus node/interface methods are such
    callables.) If raise, such instances are converted to base
    HeatingError instances carrying the same information.

    Reason: pydbus-wise, we map only HeatingError onto its dbus
    equivalent, and not a comprehensive list of all derived errors.

    '''
    def wrapper(*args):
        try:
            return fun(*args)
        except HeatingError as e:
            raise DBusHeatingError(e.details)

    return wrapper

def define_node(klass, interfaces):
    NodeDefinition(interfaces).apply_to(klass)

class NodeDefinition:
    '''DBus objects generally provide more than one interface, and one
    interface is generally provided by more than one object.

    This class combines multiple interfaces (their XML fragments) into
    one <node> definition which is then applied to a class - adding
    the "dbus" attribute that pydbus requires a class to have.

    '''

    def __init__(self, interfaces):
        self.__interfaces = interfaces

    def to_xml(self):
        ret = '<node>\n'
        for i in self.__interfaces:
            ret += i
            ret += '\n'
        ret += '</node>\n'
        return ret

    def apply_to(self, klass):
        klass.dbus = self.to_xml()
