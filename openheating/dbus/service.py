from .object import DBusObject
from .rebind import DBusServerConnection
from .thermometer_object import DBusThermometerObject

from ..testutils.thermometer import TestThermometer

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from abc import ABCMeta, abstractmethod
import signal
import time
import logging
import sys
import os


class DBusService:
    def __init__(self, daemon_address, name, object_creators):
        self.__daemon_address = daemon_address
        self.__name = name
        self.__object_creators = object_creators

        self.__restarter_pid = None

        # early sanity, rather than late after fork()
        for path, creator in self.__object_creators.items():
            assert type(path) is str
            assert isinstance(creator, DBusObjectCreator)

    def start(self):
        self.__restarter_pid = os.fork()
        if self.__restarter_pid != 0:
            return

        # child: the "restarter" process. 

        # whatever the signal disposition is, we don't want any
        # special handling.
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGQUIT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # open a process group where the service processes
        # belong. this allows us to comfortably wipe everything from
        # the parent.
        os.setpgid(0, 0)

        while True:
            service_pid = os.fork()
            if service_pid != 0:
                # parent; the "restarter". wait for child (service),
                # and backoff before restart
                died, status = os.wait()
                logging.warning('service process %d died, status %d' % (died, status))
                time.sleep(2)
                continue

            # grandchild, the service itself.

            # setup dbus bahoowazoo, create objects, and run the event
            # loop.
            try:
                print("service-child: starting")
                mainloop = DBusGMainLoop(set_as_default=True)
                dbus_connection = dbus.bus.BusConnection(self.__daemon_address, mainloop=mainloop)
                dbus_connection.set_exit_on_disconnect(True)

                print("service-child: connected")
                print("service-child: name "+self.__name)

                bus_name = dbus.service.BusName(self.__name, dbus_connection)
                connection = DBusServerConnection(connection=dbus_connection)

                objects = []
                for path, creator in self.__object_creators.items():
                    objects.append(creator.create(connection=connection, path=path))
    
                print("service-child: run")
                GLib.MainLoop().run()
                print("service-child: exit")
                sys.exit(0)
                
            except Exception as e:
                logging.exception(str(e))
                sys.exit(1)

    def stop(self):
        if self.__restarter_pid:
            os.killpg(self.__restarter_pid, signal.SIGTERM)

            # wait until they're gone. would be better to check that
            # the dbus service is gone though, by connecting and
            # looking something up.
            os.kill(self.__restarter_pid, 0)
            signal.alarm(5)
            os.waitpid(self.__restarter_pid, 0)
            signal.alarm(0)

            self.__restarter_pid = None

                
class DBusObjectCreator(metaclass=ABCMeta):
    @abstractmethod
    def create(self, connection, path):
        pass

class TestThermometerCreator(DBusObjectCreator):
    def __init__(self, initial_temperature):
        self.__initial_temperature = initial_temperature
    def create(self, connection, path):
        return DBusThermometerObject(
            connection=connection,
            path=path,
            thermometer=TestThermometer(initial_temperature=self.__initial_temperature))
