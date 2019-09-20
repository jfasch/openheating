from .object import ServerObject

import dbussy
import ravel

import signal
import asyncio
import logging


class Connection:
    def __init__(self, is_session, busname=None):
        if is_session:
            self.__connection = ravel.session_bus()
        else:
            self.__connection = ravel.system_bus()

        if busname is not None:
            self.__connection.request_name(
                bus_name=busname, 
                flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)

    def get_client_proxy(self, busname, path, iface):
        service = self.__connection[busname]
        obj = service[path]
        return obj.get_interface(iface)

    async def run(self, objects):
        """Start the objects, register them at their paths, run the loop,
        handle graceful termination by SIGINT and SIGTERM (thereby
        shutting the objects down).

        """

        loop = asyncio.get_event_loop()

        for path, obj in objects.items():
            if isinstance(obj, ServerObject):
                logging.debug('starting object on {}'.format(path))
                obj.startup(loop=loop)

        for path, obj in objects.items():
            logging.debug('registering object on {}'.format(path))
            self.__connection.register(
                path=path,
                fallback=False,
                interface=obj)


        self.__connection.attach_asyncio(loop=loop)
        future_termination = loop.create_future()

        def callback():
            future_termination.set_result(True)
        loop.add_signal_handler(signal.SIGINT, callback)
        loop.add_signal_handler(signal.SIGTERM, callback)

        try:
            logging.info('running ...')
            await future_termination
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            loop.remove_signal_handler(signal.SIGTERM)

        for path, obj in objects.items():
            if isinstance(obj, ServerObject):
                logging.debug('shutting down object on {}'.format(path))
                obj.shutdown()
