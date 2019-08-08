import dbussy
import ravel

import signal
import asyncio


class Connection:
    def __init__(self, is_session, busname=None):
        if is_session:
            self.connection = ravel.session_bus()
        else:
            self.connection = ravel.system_bus()

        if busname is not None:
            self.connection.request_name(
                bus_name=busname, 
                flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)

    def register_object(self, path, object):
        self.connection.register(
            path=path,
            fallback=False,
            interface=object)

    def get_peer(self, busname, path, iface):
        service = self.connection[busname]
        obj = service[path]
        return obj.get_interface(iface)

    async def run(self, loop):
        """Run the loop, handling graceful termination by SIGINT and SIGTERM.
        """

        self.connection.attach_asyncio(loop=loop)
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

    
