from ..thermometer import Thermometer
from ..error import HeatingError, TransientThermometerError, PermanentThermometerError

from dbus.exceptions import DBusException

#DBusException.include_traceback = True

DBUS_THERMOMETER_IFACE_STRING = 'org.openheating.Thermometer'


class _DBus_PermanentThermometerError(DBusException):
    NAME = 'org.openheating.PermanentThermometerError'
    def __init__(self, msg):
        DBusException.__init__(self, msg, name=self.NAME)
class _DBus_TransientThermometerError(DBusException):
    NAME = 'org.openheating.TransientThermometerError'
    def __init__(self, msg):
        DBusException.__init__(self, msg, name=self.NAME)
class _DBus_HeatingError(DBusException):
    NAME = 'org.openheating.HeatingError'
    def __init__(self, msg):
        DBusException.__init__(self, msg, name=self.NAME)
class _DBus_UnknownError(DBusException):
    NAME = 'org.openheating.UnknownError'
    def __init__(self, msg):
        DBusException.__init__(self, msg, name=self.NAME)



def exception_dbus_to_local(e):
    exc_name = e.get_dbus_name()
    exc_msg = e.get_dbus_message()
    
    if exc_name == _DBus_PermanentThermometerError.NAME:
        return PermanentThermometerError(exc_msg)
    if exc_name == _DBus_TransientThermometerError.NAME:
        return TransientThermometerError(exc_msg)
    if exc_name == _DBus_HeatingError.NAME:
        return HeatingError(_DBus_HeatingError.NAME+': '+exc_name+', "'+exc_msg+'"')

    # whenever we receive an exception other than HeatingError (for
    # example an AssertionError or even NameError), then this should
    # be detected the hard way. not very polite (we are crashed by the
    # remote side), but very helpful during debugging.
    assert False, 'refusing to accept any foreign errors'

    return HeatingError(_DBus_UnknownError.NAME+': '+exc_name+', "'+exc_msg+'"')

def exception_local_to_dbus(e):
    if isinstance(e, PermanentThermometerError):
        return _DBus_PermanentThermometerError(_make_original_string(e))
    if isinstance(e, TransientThermometerError):
        return _DBus_TransientThermometerError(_make_original_string(e))
    if isinstance(e, HeatingError):
        return _DBus_HeatingError(_make_original_string(e))

    assert False, 'cannot convert types other than '+str(HeatingError)+' (was: '+str(e)+')'

def _make_original_string(e):
    orstr = 'Original error:\n  ' + str(e).replace('\n', '\n  ')
    return orstr
