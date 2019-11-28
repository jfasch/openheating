from . import names



_repo = {}
def get(*ifacenames):
    ret = []
    for n in ifacenames:
        ret.append((n, _repo[n]))
    return ret


THERMOMETER = names.DOMAIN + '.Thermometer'
_repo[THERMOMETER] = '''
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
'''.format(name=THERMOMETER)

SWITCH = names.DOMAIN + '.Switch'
_repo[SWITCH] = '''
<interface name='{name}'>
  <method name='get_name'>
    <arg type='s' name='response' direction='out'/>
  </method>
  <method name='get_description'>
    <arg type='s' name='response' direction='out'/>
  </method>
  <method name='set_state'>
    <arg type='b' name='state' direction='in'/>
  </method>
  <method name='get_state'>
    <arg type='b' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=SWITCH)

SWITCHCENTER = names.DOMAIN + '.SwitchCenter'
_repo[SWITCHCENTER] = '''
<interface name='{name}'>
  <method name='all_names'>
    <arg type='as' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=SWITCHCENTER)

ERROREMITTER = names.DOMAIN + '.ErrorEmitter'
_repo[ERROREMITTER] = '''
<interface name='{name}'>
  <signal name="error">
    <arg type="s" name="what" direction="out"/>
  </signal>
</interface>
'''.format(name=ERROREMITTER)

TEMPERATUREHISTORY = names.DOMAIN + '.TemperatureHistory'
_repo[TEMPERATUREHISTORY] = '''
<interface name='{name}'>
  <method name='distill'>
    <arg type='t' name='granularity' direction='in'/>
    <arg type='t' name='duration' direction='in'/>
    <arg type='a(td)' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=TEMPERATUREHISTORY)

THERMOMETERCENTER = names.DOMAIN + '.ThermometerCenter'
_repo[THERMOMETERCENTER] = '''
<interface name='{name}'>
  <method name='all_names'>
    <arg type='as' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=THERMOMETERCENTER)

ERRORS = names.DOMAIN + '.Errors'
_repo[ERRORS] = '''
<interface name='{name}'>
  <method name='num_errors'>
    <arg type='t' name='response' direction='out'/>
  </method>
  <method name='get_errors'>
    <arg type='as' name='response' direction='out'/>
  </method>
</interface>
'''.format(name=ERRORS)

EXCEPTIONTESTER = names.DOMAIN + '.ExceptionTester'
_repo[EXCEPTIONTESTER] = '''
<interface name='{name}'>
  <method name='raise_default_HeatingError'>
    <arg type='s' name='msg' direction='in'/>
  </method>
  <method name='raise_derived_default_HeatingError'>
    <arg type='s' name='msg' direction='in'/>
  </method>
  <method name='raise_non_HeatingError'>
  </method>
</interface>
'''.format(name=EXCEPTIONTESTER)

