from .object import DBusObject
from .rebind import DBusServerConnection
from .thermometer_object import DBusThermometerObject
from .thermometer_client import DBusThermometer
from .thermometer_center_object import DBusThermometerCenterObject
from .switch_object import DBusSwitchObject
from .switch_client import DBusSwitch
from .switch_center_object import DBusSwitchCenterObject

from ..switch_center import SwitchCenter
from ..thermometer_center import ThermometerCenter

from ..testutils.thermometer import TestThermometer
from ..testutils.switch import TestSwitch
from ..hardware.gpio import create as create_gpio
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..hardware.switch_gpio import GPIOSwitch

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from abc import ABCMeta, abstractmethod
import signal
import time
import logging
import sys
import os
import errno


class DBusService:
    def __init__(self, daemon_address, name, object_creators):
        self.__daemon_address = daemon_address
        self.__name = name
        self.__object_creators = object_creators

        self.__restarter_pid = None

        # early sanity, rather than late after fork()
        for path, creator in self.__object_creators.items():
            assert type(path) is str
            assert isinstance(creator, Creator), (name, path, creator)

    def start(self):
        self.__restarter_pid = os.fork()
        if self.__restarter_pid == 0:
            self.__restarter()
            assert False, 'should never get here'

    def stop(self):
        if self.__restarter_pid is not None:
            try:
                os.kill(self.__restarter_pid, signal.SIGTERM)

                # wait until they're gone. would be better to check that
                # the dbus service is gone though, by connecting and
                # looking something up.
                signal.alarm(5)
                os.waitpid(self.__restarter_pid, 0)
                signal.alarm(0)
                    
            except ProcessLookupError:
                pass
            except Exception as e:
                assert False

            self.__restarter_pid = None

    def __restarter(self):
        # child: the "restarter" process. 

        signal.signal(signal.SIGTERM, _restarter_terminate)
        signal.signal(signal.SIGINT, _restarter_terminate)

        global _restarter_running
        _restarter_running = True
        while _restarter_running:
            service_pid = os.fork()
            if service_pid == 0:
                # child; the service
                self.__service()
                assert False, 'should never get here'
            else:
                # parent; the "restarter". wait for child (service),
                # and backoff before restart
                try:
                    died, status = os.waitpid(service_pid, 0)
                    logging.warning('service process %d died, status %d' % (died, status))
                    time.sleep(2)
                except KeyboardInterrupt:
                    pass
                except OSError as e:
                    if e.errno == errno.EINTR:
                        pass
                    else:
                        raise
        os._exit(0)

    def __service(self):
        # grandchild, the service itself.

        # setup dbus bahoowazoo, create objects, and run the event
        # loop.
        try:
            mainloop = DBusGMainLoop(set_as_default=True)
            dbus_connection = dbus.bus.BusConnection(self.__daemon_address, mainloop=mainloop)
            dbus_connection.set_exit_on_disconnect(True)

            bus_name = dbus.service.BusName(self.__name, dbus_connection)
            connection = DBusServerConnection(connection=dbus_connection)

            objects = []
            for path, creator in self.__object_creators.items():
                objects.append(creator.create_dbus_object(connection=connection, path=path))

            try:
                GLib.MainLoop().run()
            except KeyboardInterrupt:
                pass
            os._exit(0)
            
        except Exception as e:
            logging.exception(str(e))
            os._exit(1)

_restarter_running = False
def _restarter_terminate(signum, frame):
    global _restarter_running
    _restarter_running = False

# ----------------------------------------------------------------
class Creator(metaclass=ABCMeta):
    @abstractmethod
    def create_dbus_object(self, connection, path):
        pass
    @abstractmethod
    def create_native_object(self, connection):
        pass

# ----------------------------------------------------------------
class ThermometerCreator(Creator):
    def create_dbus_object(self, connection, path):
        return DBusThermometerObject(
            connection=connection,
            path=path,
            thermometer=self.create_native_object(connection))

class TestThermometerCreator(ThermometerCreator):
    def __init__(self, initial_temperature):
        self.__initial_temperature = initial_temperature
    def create_native_object(self, connection):
        return TestThermometer(initial_temperature=self.__initial_temperature)

class HWMON_I2C_ThermometerCreator(ThermometerCreator):
    def __init__(self, bus_number, address):
        self.__bus_number = bus_number
        self.__address = address
    def create_native_object(self, connection):
        return HWMON_I2C_Thermometer(bus_number=self.__bus_number, address=self.__address)

class DBusThermometerCreator(ThermometerCreator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create_native_object(self, connection):
        return DBusThermometer(connection=connection, name=self.__name, path=self.__path)

# ----------------------------------------------------------------
class SwitchCreator(Creator):
    def create_dbus_object(self, connection, path):
        return DBusSwitchObject(
            connection=connection,
            path=path,
            switch=self.create_native_object(connection))

class TestSwitchCreator(SwitchCreator):
    def __init__(self, name, initial_state):
        self.__name = name
        self.__initial_state = initial_state
    def create_native_object(self, connection):
        return TestSwitch(name=self.__name, initial_state=self.__initial_state)

class DBusSwitchCreator(SwitchCreator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create_native_object(self, connection):
        return DBusSwitch(connection=connection, name=self.__name, path=self.__path)

class GPIOSwitchCreator(SwitchCreator):
    def __init__(self, gpio_number):
        self.__gpio_number = gpio_number
    def create_native_object(self, connection):
        return GPIOSwitch(gpio=create_gpio(self.__gpio_number))

# ----------------------------------------------------------------
class ThermometerCenterCreator(Creator):
    def __init__(self, cache_age, thermometers):
        self.__cache_age = cache_age
        self.__thermometer_creators = thermometers
        
        # force type safety early
        for k, v in self.__thermometer_creators.items():
            assert type(k) is str
            assert isinstance(v, ThermometerCreator)

    def create_dbus_object(self, connection, path):
        return DBusThermometerCenterObject(
            connection=connection,
            path=path,
            center=self.create_native_object(connection))

    def create_native_object(self, connection):
        return ThermometerCenter(
            cache_age=self.__cache_age,
            thermometers={name: creator.create_native_object(connection) \
                          for name, creator in self.__thermometer_creators.items()})

# ----------------------------------------------------------------
class SwitchCenterCreator(Creator):
    def __init__(self, switches):
        self.__switch_creators = switches

        # force type safety early
        for k, v in self.__switch_creators.items():
            assert type(k) is str
            assert isinstance(v, SwitchCreator)
        
    def create_dbus_object(self, connection, path):
        return DBusSwitchCenterObject(
            connection=connection,
            path=path,
            center=self.create_native_object(connection))

    def create_native_object(self, connection):
        return SwitchCenter(
            switches={name: creator.create_native_object(connection) \
                      for name, creator in self.__switch_creators.items()})
