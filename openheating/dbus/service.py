from .object import DBusObject
from .service_config_object import DBusObjectCreator
from .connection import DBusServerConnection

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

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

            # create the bus connection wrapper that we all use, and
            # make it available for all objects and clients here in
            # this process.
            DBusServerConnection.instance = DBusServerConnection(connection=dbus_connection)

            objects = []
            for path, creator in self.__object_creators.items():
                objects.append(creator.create_object(path=path))

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
    if _service_pid is not None:
        os.kill(_service_pid, signal.SIGTERM)
    os._exit(0)

