from ..thermometer import Thermometer
from ..error import HeatingError

from dbus.exceptions import DBusException



#DBusException.include_traceback = True

DBUS_THERMOMETER_IFACE_STRING = 'org.openheating.Thermometer'


class _DBus_Thermometer_PermanentError(DBusException):
    NAME = 'org.openheating.Thermometer.PermanentError'
    def __init__(self, msg):
        DBusException.__init__(self, msg, name=self.NAME)
class _DBus_Thermometer_TransientError(DBusException):
    NAME = 'org.openheating.Thermometer.TransientError'
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
    type_name, msg = str(e).split(None, 1)
#    print('jjjj name:', type_name, 'msg:>>>>>>>>>>>>>', msg, '<<<<<<<<<<<<<')
    if type_name == _DBus_Thermometer_PermanentError.NAME:
        return Thermometer.PermanentError(msg)
    if type_name == _DBus_Thermometer_TransientError.NAME:
        return Thermometer.TransientError(msg)
    if type_name == _DBus_HeatingError.NAME:
        return HeatingError(_DBus_HeatingError.NAME+': '+type_name+', "'+msg+'"')
    return HeatingError(_DBus_UnknownError.NAME+': '+type_name+', "'+msg+'"')

def exception_local_to_dbus(e):
    assert isinstance(e, HeatingError), 'cannot convert types other than '+str(HeatingError)

    if e is Thermometer.PermanentError:
        return _DBus_Thermometer_PermanentError(_make_original_string(e))
    if e is Thermometer.TransientError:
        return _DBus_Thermometer_TransientError(_make_original_string(e))
    if e is HeatingError:
        return _DBus_HeatingError(_make_original_string(e))
    return _DBus_UnknownError(_make_original_string(e))

def _make_original_string(e):
    orstr = 'Original error:\n  ' + str(e).replace('\n', '\n  ')
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj\n', orstr)
    return orstr
