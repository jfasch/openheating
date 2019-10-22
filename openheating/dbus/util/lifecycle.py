from gi.repository import GLib

import logging
import signal
import os


lifecycle_logger = logging.getLogger('lifecycle')

class GracefulTermination:
    '''Terminate event loop when one of a set of signals arrives.

    Can be used as a 'with' context manager, setting up signal
    handlers on entry, and clearing them on exit.

    Implements the 'self pipe trick',
    http://man7.org/tlpi/code/online/diff/altio/self_pipe.c.html, to
    regularly and safely inject the termination request into the loop.

    '''

    def __init__(self, loop, signals):
        self.__loop = loop
        self.__requested = False
        self.__signals = list(signals)

        # I'd rather use eventfd(2), but a pipe is more readily
        # available in python.
        self.__pipe = os.pipe()
        # doing the self pipe trick, we watch pipe[0] (the
        # read-side). glib hands us a 'tag' which is used to remove
        # the watch later.
        self.__rfd_tag = None

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, *args):
        self.uninstall()
        return False # dont suppress exceptions

    @property
    def requested(self):
        return self.__requested

    def install(self):
        for sig in self.__signals:
            signal.signal(sig, self.__sighandler)
            r,_ = self.__pipe
        self.__rfd_tag = GLib.io_add_watch(r, GLib.IO_IN, self.__terminate_iocallback)

    def uninstall(self):
        r,_ = self.__pipe
        ok = GLib.source_remove(self.__rfd_tag)
        assert ok

        for sig in self.__signals:
            signal.signal(sig, signal.SIG_DFL)

    def __sighandler(self, signal, frame):
        lifecycle_logger.info('signal {} received, sending termination request'.format(signal))
        self.__requested = True
        _,w = self.__pipe
        os.write(w,b'q')

    def __terminate_iocallback(self, source, condition):
        lifecycle_logger.info('termination request seen, terminating')
        r,_ = self.__pipe
        # paranoia
        assert source == r
        assert condition == GLib.IO_IN

        # read from pipe so event does not keep firing
        os.read(r, 1)

        self.__loop.quit()
        return True # keep watching

class managed:
    '''Class decorator to mark a class as participating in the
    startup/shutdown game

    hooks:

    * startup: called before object is visible on the bus

    * shutdown: called before shutdown (object still visible)

    * onbus: called when object is visible on the bus, after the
      connection's bus name (if any) has been requested.

    '''

    def __init__(self, startup=None, shutdown=None, onbus=None):
        self.__startup = startup
        self.__shutdown = shutdown
        self.__onbus = onbus

    def __call__(self, cls):
        startup = shutdown = None
        if self.__startup is not None:
            cls._oh_lifecycle_startup = getattr(cls, self.__startup)
        if self.__shutdown is not None:
            cls._oh_lifecycle_shutdown = getattr(cls, self.__shutdown)
        if self.__onbus is not None:
            cls._oh_lifecycle_onbus = getattr(cls, self.__onbus)
        return cls

def run_server(loop, bus, busname, objects=None, signals=None):
    '''Run DBus server.

    * request busname
    * publish objects (and manage their lifecycle)
    * subscribe for signals
    '''

    with GracefulTermination(loop=loop, signals=(signal.SIGINT, signal.SIGTERM, signal.SIGQUIT)):
        lifecycle_logger.info('starting objects')

        if objects is None:
            objects = []
        if signals is None:
            signals = []

        for _, o in objects:
            startup = getattr(o, '_oh_lifecycle_startup', None)
            if startup is not None:
                startup()

        for path, object in objects:
            bus.register_object(path, object, None)
        for match, func in signals:
            bus.subscribe(
            iface=match.interface,
                signal=match.name,
                signal_fired=func)

        if busname is not None:
            bus.request_name(busname)

        for _, o in objects:
            onbus = getattr(o, '_oh_lifecycle_onbus', None)
            if onbus is not None:
                onbus()

        loop.run()

        lifecycle_logger.info('stopping objects')
        for _, o in objects:
            shutdown = getattr(o, '_oh_lifecycle_shutdown', None)
            if shutdown is not None:
                shutdown()

