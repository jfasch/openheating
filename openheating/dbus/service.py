from .object import DBusObject
from .rebind import DBusServerConnection
from .rebind import DBusObjectClient
from .thermometer_object import DBusThermometerObject
from .thermometer_client import DBusThermometerClient
from .thermometer_center_object import DBusThermometerCenterObject
from .switch_object import DBusSwitchObject
from .switch_client import DBusSwitchClient
from .switch_center_object import DBusSwitchCenterObject

from ..switch_center import SwitchCenter
from ..thermometer_center import ThermometerCenter

from ..testutils.test_thermometer import TestThermometer
from ..testutils.test_switch import TestSwitch
from ..testutils.file_thermometer import FileThermometer
from ..testutils.file_switch import FileSwitch

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
            assert isinstance(creator, DBusObjectCreator), (name, path, creator)

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

        global _service_pid

        while True:
            _service_pid = os.fork()
            if _service_pid == 0:
                # grandchild, the service. on shutdown, the restarter
                # will simply SIGTERM it, so I have to reset signal
                # disposition to their defaults.
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                
                self.__service()
                assert False, 'should never get here'
            else:
                # parent; the "restarter". wait for child (service),
                # and backoff before restart
                try:
                    died, status = os.waitpid(_service_pid, 0)
                    logging.warning('service process %d died, status %d' % (died, status))
                    _service_pid = None
                    time.sleep(2)
                except KeyboardInterrupt:
                    pass
                except OSError as e:
                    if e.errno == errno.EINTR:
                        # whatever that could be, we don't care.
                        pass
                    else:
                        raise

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

            # make the connection available for all DBusObjectClient
            # instances in this service.
            DBusObjectClient.service_dbus_connection = connection

            objects = []
            for path, creator in self.__object_creators.items():
                objects.append(creator.create_object(connection=connection, path=path))

            try:
                GLib.MainLoop().run()
            except KeyboardInterrupt:
                pass
            os._exit(0)
            
        except Exception as e:
            logging.exception(str(e))
            os._exit(1)

_service_pid = None

def _restarter_terminate(signum, frame):
    global _service_pid
    os.kill(_service_pid, signal.SIGTERM)
    os._exit(0)

# ----------------------------------------------------------------
class DBusObjectCreator(metaclass=ABCMeta):
    @abstractmethod
    def create_object(self, connection, path):
        pass

# ----------------------------------------------------------------
class ThermometerObjectCreator(DBusObjectCreator):
    def create_object(self, connection, path):
        return DBusThermometerObject(
            connection=connection,
            path=path,
            thermometer=self.create_native_object(connection))

class TestThermometerObjectCreator(ThermometerObjectCreator):
    def __init__(self, initial_temperature):
        self.__initial_temperature = initial_temperature
    def create_native_object(self, connection):
        return TestThermometer(initial_temperature=self.__initial_temperature)

class FileThermometerObjectCreator(ThermometerObjectCreator):
    def __init__(self, path):
        self.__path = path
    def create_native_object(self, connection):
        return FileThermometer(path=self.__path)

class HWMON_I2C_ThermometerObjectCreator(ThermometerObjectCreator):
    def __init__(self, bus_number, address):
        self.__bus_number = bus_number
        self.__address = address
    def create_native_object(self, connection):
        return HWMON_I2C_Thermometer(bus_number=self.__bus_number, address=self.__address)

class DBusThermometerClientObjectCreator(ThermometerObjectCreator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create_native_object(self, connection):
        return DBusThermometerClient(connection=connection, name=self.__name, path=self.__path)

# ----------------------------------------------------------------
class SwitchObjectCreator(DBusObjectCreator):
    def create_object(self, connection, path):
        return DBusSwitchObject(
            connection=connection,
            path=path,
            switch=self.create_native_object(connection))

class TestSwitchObjectCreator(SwitchObjectCreator):
    def __init__(self, name, initial_state):
        self.__name = name
        self.__initial_state = initial_state
    def create_native_object(self, connection):
        return TestSwitch(name=self.__name, initial_state=self.__initial_state)

class FileSwitchObjectCreator(SwitchObjectCreator):
    def __init__(self, path):
        self.__path = path
    def create_native_object(self, connection):
        return FileSwitch(path=self.__path)

class DBusSwitchClientObjectCreator(SwitchObjectCreator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create_native_object(self, connection):
        return DBusSwitchClient(connection=connection, name=self.__name, path=self.__path)

class GPIOSwitchObjectCreator(SwitchObjectCreator):
    def __init__(self, gpio_number):
        self.__gpio_number = gpio_number
    def create_native_object(self, connection):
        return GPIOSwitch(gpio=create_gpio(self.__gpio_number))

# ----------------------------------------------------------------
class ThermometerCenterObjectCreator(DBusObjectCreator):
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def create_object(self, connection, path):
        return DBusThermometerCenterObject(
            connection=connection,
            path=path,
            center=ThermometerCenter(self.__thermometers))

# ----------------------------------------------------------------
class SwitchCenterObjectCreator(DBusObjectCreator):
    def __init__(self, switches):
        self.__switches = switches
        
    def create_object(self, connection, path):
        return DBusSwitchCenterObject(
            connection=connection,
            path=path,
            center=SwitchCenter(self.__switches))
