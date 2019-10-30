from ..error import HeatingError
from .util import lifecycle as jjj_lifecycle

from pydbus import SystemBus, SessionBus

import json
import signal
import logging


def argparse_add_bus(parser):
    '''add --session|--system options to commandline parsing'''

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus_from_argparse(args):
    '''given --session|--system is in argparse, connect to the respective
    bus, and return the bus object'''

    return args.session and SessionBus() or SystemBus()


# centrally defined names, to ease modifications
DOMAIN = 'org.openheating'

# bus names
THERMOMETERS_BUSNAME = DOMAIN + '.Thermometers'
ERRORS_BUSNAME = DOMAIN + '.Errors'
EXCEPTIONTESTER_BUSNAME = DOMAIN + '.ExceptionTester'
MANAGEDOBJECTTESTER_BUSNAME = DOMAIN + '.ManagedObjectTester'

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

ERRORS_IFACENAME = DOMAIN + '.Errors'
ERRORS_IFACEXML = '''
<interface name='{name}'>
  <method name='num_errors'>
    <arg type='t' name='response' direction='out'/>
  </method>
  <method name='get_errors'>
    <arg type='as' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=ERRORS_IFACENAME)

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
        return self.to_json()

    def to_json(self):
        return json.dumps(self.details)

    @staticmethod
    def from_json(js):
        details = json.loads(js)
        return DBusHeatingError(details=details)

