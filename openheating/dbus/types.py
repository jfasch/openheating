from ..thermometer import Thermometer
from ..error import HeatingError

from dbus.exceptions import DBusException

#DBusException.include_traceback = True

DBUS_THERMOMETER_IFACE_STRING = 'org.openheating.Thermometer'
DBUS_THERMOMETER_CENTER_IFACE_STRING = 'org.openheating.ThermometerCenter'

DBUS_SWITCH_IFACE_STRING = 'org.openheating.Switch'
DBUS_SWITCH_CENTER_IFACE_STRING = 'org.openheating.SwitchCenter'

DBUS_HEATING_ERROR_NAME = 'org.openheating.HeatingError'

def exception_dbus_to_local(e):
    exc_name = e.get_dbus_name()
    exc_msg = e.get_dbus_message()

    # whenever we receive an exception other than HeatingError (for
    # example an AssertionError or even NameError), then this should
    # be detected the hard way. not very polite (we are crashed by the
    # remote side), but very helpful during debugging.
    assert exc_name == 'org.openheating.HeatingError', \
        'refusing to accept any foreign DBus errors: name=' + exc_name + ', msg=' + exc_msg
    return HeatingError(exc_msg)

def exception_local_to_dbus(e):
    assert isinstance(e, HeatingError)
    return DBusException(e.msg(), name=DBUS_HEATING_ERROR_NAME)
