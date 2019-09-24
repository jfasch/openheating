from . import names
from . import ifaces
from .object import ServerObject
from ..thermometer import Thermometer
from ..error import HeatingError
from .. import logutil

import ravel

from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
import logging


logger = logging.getLogger('dbus-thermometer')

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


@ifaces.THERMOMETER.iface
class Thermometer_Server(ServerObject):
    def __init__(self, update_interval, thermometer, history):
        assert isinstance(thermometer, Thermometer)

        self.__update_interval = update_interval
        self.__thermometer = thermometer
        self.__current_temperature = self.__thermometer.get_temperature()
        self.__history = history

        # schedule periodic temperature updates in a background
        # thread.

        # reason: w1_slave's filenum cannot be used asynchronously. at
        # the time the fd's read callback is triggered, and you
        # os.read() from it, that read will start bitbanging and the
        # call will take approximately a second just as if we had
        # called it synchronously.
        self.__executor = None
        self.__update_task = None

    @ifaces.THERMOMETER.get_name
    def get_name(self):
        return (self.__thermometer.get_name(),)

    @ifaces.THERMOMETER.get_description
    def get_description(self):
        return (self.__thermometer.description,)

    @ifaces.THERMOMETER.get_temperature
    def get_temperature(self):
        if self.__current_temperature is None:
            raise ravel.ErrorReturn(name=names.EXCEPTION.HEATINGERROR, message='no current value')
        return (self.__current_temperature,)

    def startup(self, loop):
        self.__executor = ThreadPoolExecutor(max_workers=1)
        self.__update_task = loop.create_task(logutil.handle_task_exceptions(self.__periodic_update()))

    def shutdown(self):
        self.__update_task.cancel()
        self.__executor.shutdown()

        self.__update_task = None
        self.__executor = None

    async def __periodic_update(self):
        loop = asyncio.get_event_loop()
        while True:
            await asyncio.sleep(self.__update_interval)
            try:
                new_temperature = await loop.run_in_executor(
                    self.__executor, self.__thermometer.get_temperature)
            except HeatingError:
                try:
                    logger.exception('{}: cannot get temperature'.format(self.__thermometer.get_name()))
                except Exception as e:
                    raise
            else:
                self.__new_temperature(new_temperature)
                logger.info('{}: updated temperature ({}C)'.format(self.__thermometer.get_name(), self.__current_temperature))

    def __new_temperature(self, temperature):
        self.__current_temperature = temperature
        now = time.time()
        self.__history.add(timestamp=now, value=temperature)
