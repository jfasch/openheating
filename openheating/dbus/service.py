import signal
import asyncio

import ravel
import dbussy


def create_connection(busname, is_session, loop):
    """Create DBus connection, glue it into asyncio, and request busname
    for it

    :param busname str: connection name on the bus
    :param is_session bool: use session bus (True) or system bus (False)
    :param loop: event loop to attach to
    """

    if is_session:
        connection = ravel.session_bus()
    else:
        connection = ravel.system_bus()
    connection.attach_asyncio(loop=loop)
    connection.request_name(
        bus_name=busname, 
        flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)
    return connection

async def graceful_termination(loop):
    """Run the loop, handling graceful termination by SIGINT and SIGTERM.
    """

    future_termination = loop.create_future()

    def callback():
        future_termination.set_result(True)
    loop.add_signal_handler(signal.SIGINT, callback)
    loop.add_signal_handler(signal.SIGTERM, callback)

    try:
        await future_termination
    finally:
        loop.remove_signal_handler(signal.SIGINT)
        loop.remove_signal_handler(signal.SIGTERM)

    
