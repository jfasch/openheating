from . import names

from ..error import HeatingError

import pydbus.error

import xml.etree.ElementTree as ET
import traceback
import logging
import sys
import json


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

# map, pydbus-wise, HeatingError exceptions to their dbus error
# counterpart.
pydbus.error.error_registration.map_error(DBusHeatingError, names.HEATINGERROR)


class Definition:
    '''DBus objects generally provide more than one interface, and one
    interface is generally provided by more than one object.

    This class combines multiple interfaces (their XML fragments) into
    one <node> definition which is then applied to a class - adding
    the "dbus" attribute that pydbus requires a class to have.

    Instances are callable, thereby acting as a decorator for classes
    that implement dbus node.

    '''

    def __init__(self, interfaces):
        self.__xml = '<node>\n'
        for i in interfaces:
            self.__xml += i
            self.__xml += '\n'
        self.__xml += '</node>\n'

    @property
    def xml(self):
        return self.__xml

    def __call__(self, klass):
        'decorator functionality'

        # in klass, wrap all dbus methods to convert HeatingError
        # exceptions onto a dbus-understandable exception
        # (DBusHeatingError)
        for name, method in self.__dbus_methods(klass):
            setattr(klass, name, self.__wrap_dbus_method(method))

        # create klass.dbus attribute which provide the node
        # definition for pydbus
        assert getattr(klass, 'dbus', None) is None
        klass.dbus = self.__xml
        return klass

    def __dbus_methods(self, klass):
        ret = []
        et = ET.fromstring(self.__xml)
        for methodname in (m.get('name') for m in et.findall('./interface/method')):
            method = getattr(klass, methodname, None)
            if method is None:
                raise HeatingError('{} has no method {}'.format(klass.__name__, methodname))
            if not callable(method):
                raise HeatingError('{}.{} is not callable'.format(klass.__name__, methodname))
            ret.append((methodname, method))
        return ret

    class UnexpectedExceptionError(HeatingError):
        def __init__(self):
            tbstr = traceback.format_exc()
            super().__init__(details={'category': 'internal',
                                      'message': str(e),
                                      'traceback': tbstr})

    @classmethod
    def __wrap_dbus_method(klass, method):
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except HeatingError as e:
                raise DBusHeatingError(e.details)
            except Exception as e:
                raise DBusHeatingError(klass.UnexpectedExceptionError().details)

        return wrapper

class SignalMatch:
    def __init__(self, interface, name):
        self.interface = interface
        self.name = name
