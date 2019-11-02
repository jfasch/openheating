from . import names
from . import interface_repo

from ..base.error import HeatingError

import pydbus.error

import xml.etree.ElementTree as ET
import traceback
import logging
import sys
import json
import functools


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
    '''Class decorator for DBus node/object implementations, doing what
    follows.

    Interfaces
    ----------

    Interfaces are defined as XML fragments, like::

       <interface name='org.openheating.Thermometer'>
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

    DBus objects generally provide more than one interface, and one
    interface is generally provided by more than one object.

    This node.Definition class combines multiple interfaces (their XML
    fragments) into one <node> definition which is then applied to a
    class - adding the "dbus" attribute that pydbus requires a class
    to have.

    When applied to a class as a decorator (its intended usage), it
    figures out what methods the XML defines. All those methods have
    to be provided by the wrapped class; if not this is an
    error. Every such method is wrapped into code that translates
    HeatingError exception onto dbus exceptions, and that catches,
    logs and reports unexpected internal errors.

    Signals
    -------

    Signals, while their purpose is easily understood, are a bit,
    well, dangling, with respect to methods:

    * Emission: an object emits a signal via an interface. While the
      entire point in interfaces is to contain methods for the
      end-user to call, it is not immediately clear why the signal
      specification - for the purpose of *emitting* - has to be part
      of an interface.

    * Reception: any bus connection can declare to receive
      signals. Ideally this is done by using a filter saying for
      example "I only want to receive signals from interface
      'org.openheating.ErrorEmitter', and/or from objects hosted by
      busname org.openheating.Thermometers and/or on path
      /thermometers/Raum in that process).

    Both signal emission and reception are somewhat narrowed by
    node.Definition, by the following measures.

    Emission
    ........

    * Interface org.openheating.ErrorEmitter is implicitly added to
      every dbus node implementation. When calling server methods, we
      catch unexpected exceptions and report that fact by sending out
      a signal on said interface, so this interface has to be part of
      the node's definition.

    * All signal specifications that are found in the XML node
      definition result in an equally named pydbus.generic.signal
      class member - calling this signal (with an arbitrary set of
      parameters) is the pydbus way of emitting signals.

    * For the implicit org.openheating.ErrorEmitter interface, a
      special emit_error(HeatingError:e) convenience method is
      created.

    Reception
    .........

    jjj tbd implement first

    '''

    def __init__(self, interfaces):
        assert interface_repo.ERROREMITTER not in [name for name,_ in interfaces]
        interfaces = list(interfaces)

        # implicitly add the 'error' signal to emit HeatingError
        # instances on.
        interfaces.extend(interface_repo.get(interface_repo.ERROREMITTER))

        self.__xml = '<node>\n'
        for _,ifacexml in interfaces:
            self.__xml += ifacexml
            self.__xml += '\n'
        self.__xml += '</node>\n'

    @property
    def xml(self):
        return self.__xml

    def __call__(self, klass):
        'decorator functionality'

        et = ET.fromstring(self.__xml)

        if True:
            # in klass, wrap all dbus methods to convert HeatingError
            # exceptions to a dbus-understandable exception
            # (DBusHeatingError)

            for name, method in self.__dbus_methods(et, klass):
                setattr(klass, name, self.__wrap_dbus_method(klass, method))

        if True:
            # add signals

            assert 'error' in self.__dbus_signals(et), "predefined 'error' signal not found in XML"
            for name in self.__dbus_signals(et):
                assert getattr(klass, name, None) is None

                sig = pydbus.generic.signal()
                setattr(klass, name, sig)

                # add convenience method for sending HeatingError instances
                # out on predefined 'error' signal.
                if name == 'error':
                    assert getattr(klass, 'emit_error', None) is None
                    def emit_error_func(self, e):
                        dbus_e = DBusHeatingError(e.details)
                        # error is a class member, but I have to use
                        # self not class. else the signall is simply
                        # not emitted. gosh.
                        self.error(str(dbus_e))
                    setattr(klass, 'emit_error', emit_error_func)

        if True:
            # create klass.dbus attribute which provides the node
            # definition for pydbus

            assert getattr(klass, 'dbus', None) is None
            klass.dbus = self.__xml

        return klass

    def __dbus_methods(self, et, klass):
        ret = []
        for methodname in (m.get('name') for m in et.findall('./interface/method')):
            method = getattr(klass, methodname, None)
            if method is None:
                raise HeatingError('{} has no method {}'.format(klass.__name__, methodname))
            if not callable(method):
                raise HeatingError('{}.{} is not callable'.format(klass.__name__, methodname))
            ret.append((methodname, method))
        return ret

    def __dbus_signals(self, et):
        return [s.get('name') for s in et.findall('./interface/signal')]

    class UnexpectedExceptionError(HeatingError):
        def __init__(self):
            etype, e, tb = sys.exc_info()
            super().__init__(details={'category': 'internal',
                                      'message': str(e),
                                      'traceback': traceback.format_tb(tb),
            })

    def __wrap_dbus_method(self, klass, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):

            # pydbus signals are weird. the signal object itself must
            # be a class member, whereas the signal is only really
            # emitted if you use self to find it.
            self = args[0]

            raise_e = None
            try:
                return method(*args, **kwargs)
            except HeatingError as e:
                logging.exception('method {} error'.format(method.__name__), e)
                raise_e = DBusHeatingError(e.details)
            except Exception as e:
                logging.exception('method {} unexpected error'.format(method.__name__))
                raise_e = DBusHeatingError(Definition.UnexpectedExceptionError().details)

                # use self not class to emit signal
                self.emit_error(raise_e)

            if raise_e is not None:
                raise raise_e

        return wrapper

class SignalMatch:
    def __init__(self, interface, name):
        self.interface = interface
        self.name = name
