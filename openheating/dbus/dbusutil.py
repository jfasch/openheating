import signal


from pydbus import SystemBus, SessionBus


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
  <method name='raise_base_HeatingError'>
    <arg type='s' name='msg' direction='in'/>
  </method>
</interface>
'''.format(name=EXCEPTIONTESTER_IFACENAME)


HEATINGERROR_NAME = DOMAIN + '.HeatingError'

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
