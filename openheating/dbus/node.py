from . import dbusutil

from ..error import HeatingError

import xml.etree.ElementTree as ET


# def unify_error(fun):
#     '''Used as a decorator for callables that raise derived HeatingError
#     instances. (Generally, dbus node/interface methods are such
#     callables.) If raised, such instances are converted to base
#     HeatingError instances carrying the same information.

#     Reason: pydbus-wise, we map only HeatingError onto its dbus
#     equivalent, and not a comprehensive list of all derived errors.

#     '''
#     def wrapper(*args):
#         try:
#             return fun(*args)
#         except HeatingError as e:
#             raise dbusutil.DBusHeatingError(e.details)

#     return wrapper

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
        'descriptor functionality'

        # in klass, wrap all dbus methods to convert HeatingError
        # exceptions onto a dbus-understandable exception
        # (DBusHeatingError)
        for name, method in self.__dbus_methods(klass):
            setattr(klass, name, self.__convert_error(method))

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

    @staticmethod
    def __convert_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HeatingError as e:
                raise dbusutil.DBusHeatingError(e.details)

        return wrapper

class SignalMatch:
    def __init__(self, interface, name):
        self.interface = interface
        self.name = name
