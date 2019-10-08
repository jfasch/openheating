from . import dbusutil
from ..thermometer import Thermometer
from ..error import HeatingError
from .. import timeutil
from .. import logutil

from gi.repository import GLib
from pydbus.generic import signal

import time
import logging
from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger('dbus-thermometer')

class Thermometer_Client(Thermometer):
    def __init__(self, proxy):
        self.proxy = proxy

        self.name = None
        self.description = None

    def get_name(self):
        if self.name is None:
            self.name = self.proxy.get_name()
        return self.name

    def get_description(self):
        if self.description is None:
            self.description = self.proxy.get_description()
        return self.description

    def get_temperature(self):
        return self.proxy.get_temperature()

class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    def distill(self, granularity, duration):
        return self.__proxy.distill(
            timeutil.delta2unix(granularity), 
            timeutil.delta2unix(duration))


class Thermometer_Server:
    # errors are emitted via here
    error = signal()

    def __init__(self, update_interval, thermometer, history):
        assert isinstance(thermometer, Thermometer)

        # trusting the GIL, we don't lock these against the update
        # background thread (though we probably should anyway).
        self.__thermometer = thermometer
        # get name from thermometer once and forever, to prevent
        # errors during runtime.
        self.__name = self.__thermometer.get_name()
        self.__history = history

        self.__current_temperature = None

        # schedule periodic temperature updates in a *background
        # thread*. this is because w1 bitbanging blocks for almost a
        # second per temperature read.

        logger.info('{}: schedule temperature updates every {} seconds'.format(self.__name, update_interval))
        self.__background_thread = ThreadPoolExecutor(max_workers=1)
        GLib.timeout_add_seconds(update_interval, self.__schedule_update)

    def get_name(self):
        return self.__thermometer.get_name()

    def get_description(self):
        return self.__thermometer.get_description()

    def get_temperature(self):
        if self.__current_temperature is None:
            self.__current_temperature = self.__thermometer.get_temperature()
        return self.__current_temperature

    def distill(self, granularity, duration):
        return self.__history.distill(granularity=granularity, duration=duration)

    def __schedule_update(self):
        # submit work to the background thread, *not* waiting for the
        # returned future object (alas, we don't want to block)
        logger.debug('{}: scheduling update'.format(self.__name))
        self.__background_thread.submit(self.__update)
        return True # re-arm timer

    def __update(self):
        # in the background thread now, take as long as we want (about
        # a second) to read the temperature from the sensor. when
        # done, push what we have into the GLib main loop and do
        # further processing there (adding the value to the history,
        # emitting errors onto the bus, ...)

        # (see https://wiki.gnome.org/Projects/PyGObject/Threading for
        # what GLib.idle_add() does)

        try:
            current_temperature = self.__thermometer.get_temperature()
            GLib.idle_add(self.__receive_update, current_temperature)
        except Exception as e:
            logger.exception('{} (update-thread): thermometer error'.format(self.__name))
            GLib.idle_add(self.__receive_error, e)

        logger.debug('{} (update-thread): sensor has {} degrees; pushing into main loop'.format(
            self.__name, current_temperature))

    def __receive_update(self, current_temperature):
        logger.debug('{}: receiving temperature ({} degrees) from update-thread'.format(self.__name, current_temperature))
        self.__current_temperature = current_temperature
        self.__history.add(time.time(), current_temperature)

    def __receive_error(self, e):
        logger.debug('{}: receiving error {} from update-thread'.format(self.__name, e))
        self.error(str(e))

dbusutil.define_node(
    klass=Thermometer_Server,
    interfaces=(dbusutil.THERMOMETER_IFACEXML,
                dbusutil.TEMPERATUREHISTORY_IFACEXML,
                dbusutil.ERROREMITTER_IFACEXML))
