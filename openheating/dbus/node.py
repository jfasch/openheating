from . import dbusutil

from ..error import HeatingError


def unify_error(fun):
    '''Used as a decorator for callables that raise derived HeatingError
    instances. (Generally, dbus node/interface methods are such
    callables.) If raised, such instances are converted to base
    HeatingError instances carrying the same information.

    Reason: pydbus-wise, we map only HeatingError onto its dbus
    equivalent, and not a comprehensive list of all derived errors.

    '''
    def wrapper(*args):
        try:
            return fun(*args)
        except HeatingError as e:
            raise dbusutil.DBusHeatingError(e.details)

    return wrapper

class Definition:
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

    def __call__(self, klass):
        assert getattr(klass, 'dbus', None) is None
        klass.dbus = self.to_xml()
        return klass

class SignalMatch:
    def __init__(self, interface, name):
        self.interface = interface
        self.name = name
