import signal
import asyncio

import ravel
import dbussy


def create_connection(busname, session):
    """Create DBus connection, glue it into asyncio, and request busname
    for it

    """
    if session:
        bus = ravel.session_bus()
    else:
        bus = ravel.system_bus()
    bus.attach_asyncio()
    bus.request_name(
        bus_name=busname, 
        flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)
    return bus

async def termination():
    """Await graceful termination

    Register signal handlers for SIGINT and SIGTERM, await arrival of
    those.

    """
    loop = asyncio.get_event_loop()
    future_termination = loop.create_future()

    def callback():
        future_termination.set_result(True)
    loop.add_signal_handler(signal.SIGINT, callback)
    loop.add_signal_handler(signal.SIGTERM, callback)

    return await future_termination
