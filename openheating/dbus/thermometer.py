from . import names
from .object import ServerObject
from ..thermometer import Thermometer
from ..error import HeatingError

from concurrent.futures import ThreadPoolExecutor
import asyncio

import ravel


class Thermometer_Client(Thermometer):
    def __init__(self, proxy):
        self.proxy = proxy

        self.name = None
        self.description = None

    def get_name(self):
        if self.name is None:
            self.name = self.proxy.get_name()[0]
        return self.name

    def get_description(self):
        if self.description is None:
            self.description = self.proxy.get_description()[0]
        return self.description

    def get_temperature(self):
        return self.proxy.get_temperature()[0]


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER)
class Thermometer_Server(ServerObject):
    def __init__(self, interval, thermometer):
        assert isinstance(thermometer, Thermometer)

        self.__loop = None
        self.__update_interval = interval
        self.__thermometer = thermometer
        self.__current_temperature = self.__thermometer.get_temperature()

        # schedule periodic temperature updates in a background
        # thread.

        # reason: w1_slave's filenum cannot be used asynchronously. at
        # the time the fd's read callback is triggered, and you
        # os.read() from it, that read will start bitbanging and the
        # call will take approximately a second just as if we had
        # called it synchronously.
        self.__executor = None
        self.__update_task = None

    @ravel.method(
        name = 'get_name',
        in_signature = '',
        out_signature = 's')
    def get_name(self):
        return (self.__thermometer.get_name(),)

    @ravel.method(
        name = 'get_description',
        in_signature = '',
        out_signature = 's')
    def get_description(self):
        return (self.__thermometer.description,)

    @ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd')
    def get_temperature(self):
        try:
            return (self.__current_temperature,)
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))

    def startup(self, loop):
        self.__loop = loop
        self.__executor = ThreadPoolExecutor(max_workers=1)
        self.__update_task = self.__loop.create_task(self.__periodic_update())

    def shutdown(self):
        self.__update_task.cancel()
        self.__executor.shutdown()

        self.__update_task = None
        self.__executor = None
        self.__loop = None

    async def __periodic_update(self):
        while True:
            await asyncio.sleep(self.__update_interval)
            self.__current_temperature = await self.__loop.run_in_executor(
                self.__executor, self.__thermometer.get_temperature)
