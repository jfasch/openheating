import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from abc import ABCMeta, abstractmethod
import logging
import sys
import signal
import os
import time

class DBusServiceCombo:
    def __init__(self, pidfile, daemon_address, busname):
        self.__pidfile = pidfile
        self.__daemon_address = daemon_address
        self.__busname = busname
        self.__child = None

    def run(self):
        # there must be only one per process
        global _object
        assert _object is None

        _object = self

        signal.signal(signal.SIGTERM, _terminate_handler)
        signal.signal(signal.SIGQUIT, _terminate_handler)
        signal.signal(signal.SIGINT, _terminate_handler)

        if self.__pidfile is not None:
            open(self.__pidfile, 'w').write(str(os.getpid())+'\n')

        while True:
            self.__child = os.fork()
            if self.__child > 0:
                # parent. wait for child, and backoff before restart
                died, status = os.wait()
                logging.warning('child %d died, status %d' % (died, status))
                time.sleep(2)
            else:
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                signal.signal(signal.SIGQUIT, signal.SIG_DFL)
                signal.signal(signal.SIGINT, signal.SIG_DFL)

                try:
                    mainloop = DBusGMainLoop(set_as_default=True)
                    connection = dbus.bus.BusConnection(self.__daemon_address, mainloop=mainloop)
                    connection.set_exit_on_disconnect(True)
                    busname = dbus.service.BusName(self.__busname, connection)

                    # tell derived class to fill in what's needed
                    self.create_objects(connection)
        
                    GLib.MainLoop().run()
                except Exception as e:
                    logging.exception(str(e))
                    exit(1)

    @abstractmethod
    def create_objects(self, connection):
        pass

    def terminate(self, signum):
        # kill child. the terminate-signal could well arrive *after*
        # the child has exited and *before* it is restarted, so its
        # pid might not be valid - so we have to ignore errors.
        if self.__child is not None:
            try:
                os.kill(self.__child, signum)
            except OSError: pass
        # remove pidfile
        if self.__pidfile is not None:
            os.remove(self.__pidfile)
        sys.exit(0)

_object = None

def _terminate_handler(signum, frame):
    if _object is not None:
        _object.terminate(signum)
