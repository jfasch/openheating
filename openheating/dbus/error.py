from . import names

from ..base.error import HeatingError

import gi.repository

import functools
import json


class DBusHeatingError(HeatingError):
    '''Used to pass HeatingError exceptions across the bus.

    Use @unify_error to decorate interface method implementations,
    converting native HeatingError exceptions into a DBusHeatingError.

    DBusHeatingError then collaborates with pydbus and brings the
    error across the bus. Btw, dbus exception returne consist of the
    exception type (a string) and any number of arguments (I believe),
    of which pydbus only uses one, a string.

    * Server: on exception occurence (a server method throws), pydbus
      calls str() on it to build the dbus ERROR argument (dbus
      string). As for the exception type, pydbus asks the exception
      object for the name of its type, type(e).__name__. See
      pydbus.registration.ObjectWrapper.call_method() for details.

    * at the client, the converted errors arrive as the type we gave
      it on the server side (org.openheating.HeatingError). only the
      str argument has been mangled on its way - use the @maperror
      decorator below to solve that particular weirdness.

    '''
    def __init__(self, details):
        if type(details) is str:
            # assume it came across the bus, so it must be json. take
            # it literally.
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

# on receipt of a server object exception, pydbus sends the native
# exception type's name as the dbus exception type. monkey patch that.
DBusHeatingError.__name__ = names.HEATINGERROR
assert DBusHeatingError.__name__ == names.HEATINGERROR


def maperror(func):
    '''Decorator for client objects methods, mapping the gdbus error back
    into its original HeatingError form.

    '''
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        glib_message = None
        try:
            return func(*args, **kwargs)
        except gi.repository.GLib.GError as e:
            glib_message = e.message

        if glib_message is not None:
            # we assume that we talk to a properly defined (as per
            # node.Definition) dbus object, and expect only
            # HeatingError instances to come through. the remote type
            # manifests itself in the formatted message of the dbus
            # error. (this is a gdbus/pydbus implementation detail, so
            # this probably needs some tuning.)

            pat = 'GDBus.Error:org.openheating.HeatingError: '
            assert glib_message.find(pat) == 0, '"{}" not found in GError.message "{}"'.format(pat, glib_message)
            js = glib_message[len(pat):]
            raise HeatingError(details=json.loads(js))

    return wrapped


