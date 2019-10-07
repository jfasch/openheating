from .object import ServerObject

import dbussy
import ravel

import signal
import asyncio
import logging


logger = logging.getLogger('dbus-connection')

class Connection:
    def __init__(self, is_session, busname=None):
        logger.info('connecting to {} bus'.format(is_session and 'session' or 'system'))
        self.connection = is_session and ravel.session_bus() or ravel.system_bus()
        if busname is not None:
            self.connection.request_name(
                bus_name=busname, 
                flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)

    def get_client_proxy(self, busname, path, iface):
        service = self.connection[busname]
        obj = service[path]
        return obj.get_interface(iface)

    async def run(self, objects):
        """Start the objects, register them at their paths, add connection to
        the loop. Sit waiting for graceful termination by SIGINT and
        SIGTERM. After that, shutdown the objects.

        """

        loop = asyncio.get_event_loop()

        for path, obj in objects.items():
            if isinstance(obj, ServerObject):
                logger.debug('starting object on {}'.format(path))
                obj.startup(loop=loop)

        for path, obj in objects.items():
            logger.debug('registering object on {}'.format(path))
            self.connection.register(
                path=path,
                fallback=False,
                interface=obj)


        self.connection.attach_asyncio(loop=loop)
        future_termination = loop.create_future()

        def callback():
            future_termination.set_result(True)
        loop.add_signal_handler(signal.SIGINT, callback)
        loop.add_signal_handler(signal.SIGTERM, callback)

        try:
            logger.info('running ...')
            await future_termination
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            loop.remove_signal_handler(signal.SIGTERM)

        for path, obj in objects.items():
            if isinstance(obj, ServerObject):
                logger.debug('shutting down object on {}'.format(path))
                obj.shutdown()
