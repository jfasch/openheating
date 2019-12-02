from gi.repository import GLib

import logging
import signal
import os


lifecycle_logger = logging.getLogger('lifecycle')

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
    * subscribe for DBus signals
    '''

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

    # setup graceful termination. BIG RANT: they will only let me
    # handle a predefined set of signals which smells like ... well
    # ... like some ugly kind of bullshit is going on. read yourself:

    # lifecycle.py:177: Warning: g_unix_signal_source_new: assertion 'signum == SIGHUP || signum == SIGINT || signum == SIGTERM || signum == SIGUSR1 || signum == SIGUSR2' failed
    #   GLib.unix_signal_add(GLib.PRIORITY_HIGH, sig, _quit, sig)
    # /home/jfasch/openheating/openheating/dbus/lifecycle.py:177: Warning: g_source_set_priority: assertion 'source != NULL' failed
    #   GLib.unix_signal_add(GLib.PRIORITY_HIGH, sig, _quit, sig)
    # /home/jfasch/openheating/openheating/dbus/lifecycle.py:177: Warning: g_source_set_callback: assertion 'source != NULL' failed
    #   GLib.unix_signal_add(GLib.PRIORITY_HIGH, sig, _quit, sig)
    # Speicherzugriffsfehler

    # not that I insist in handling SIGQUIT, but ...

    def _quit(sig):
        loop.quit()
    for sig in (signal.SIGTERM, signal.SIGINT):
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, sig, _quit, sig)

    loop.run()

    lifecycle_logger.info('stopping objects')
    for _, o in objects:
        shutdown = getattr(o, '_oh_lifecycle_shutdown', None)
        if shutdown is not None:
            shutdown()

