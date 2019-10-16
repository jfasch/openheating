from . import dbusutil

from pydbus.error import error_registration


# map, pydbus-wise, HeatingError exceptions to their dbus error
# counterpart.
error_registration.map_error(dbusutil.DBusHeatingError, dbusutil.HEATINGERROR_NAME)
