from . import interface_repo
from . import node
from . import error
from . import lifecycle

from ..base.thermometer import Thermometer
from ..base.error import HeatingError
from ..base import timeutil

from gi.repository import GLib
from pydbus.generic import signal

import time
import logging
from concurrent.futures import ThreadPoolExecutor


class Thermometer_Client(Thermometer):
    def __init__(self, proxy):
        self.proxy = proxy

        self.name = None
        self.description = None

    @error.maperror
    def get_name(self):
        if self.name is None:
            self.name = self.proxy.get_name()
        return self.name

    @error.maperror
    def get_description(self):
        if self.description is None:
            self.description = self.proxy.get_description()
        return self.description

    @error.maperror
    def get_temperature(self):
        return self.proxy.get_temperature()

    @error.maperror
    def force_update(self, timestamp):
        self.proxy.force_update(timestamp)

class TemperatureHistory_Client:
    def __init__(self, proxy):
        self.__proxy = proxy

    @error.maperror
    def distill(self, granularity, duration):
        return self.__proxy.distill(
            timeutil.delta2unix(granularity), 
            timeutil.delta2unix(duration))


@lifecycle.managed(startup='_startup', shutdown='_shutdown', onbus='_onbus')
@node.Definition(interfaces=interface_repo.get(interface_repo.THERMOMETER, 
                                               interface_repo.TEMPERATUREHISTORY))
class Thermometer_Server:
    def __init__(self, name, description, thermometer, update_interval, history):
        assert isinstance(thermometer, Thermometer)

        self.__name = name
        self.__description = description
        self.__thermometer = thermometer

        self.__history = history

        self.__current_temperature = None
        self.__current_error = HeatingError('reading temperature too early, not yet initialized')

        # schedule periodic temperature updates in a *background
        # thread*. this is because w1 bitbanging blocks for almost a
        # second per temperature read.
        self.__background_thread = None
        self.__update_interval = update_interval
        self.__update_timer_tag = None

        self.__logger = logging.getLogger(self.__name)

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_temperature(self):
        if self.__current_error:
            raise self.__current_error
        return self.__current_temperature

    def force_update(self, timestamp):
        if self.__update_interval != 0:
            raise HeatingError('cannot force_update when doing background updates')
        self.__make_current(timestamp=timestamp, temperature=self.__thermometer.get_temperature())

    def distill(self, granularity, duration):
        return list(self.__history.distill(granularity=granularity, duration=duration))

    def __schedule_update(self):
        # submit work to the background thread, *not* waiting for the
        # returned future object (alas, we don't want to block)
        self.__logger.debug('scheduling update')
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
            self.__logger.debug('(update-thread): sensor has {} degrees'.format(current_temperature))
            GLib.idle_add(self.__receive_update, time.time(), current_temperature, None)
        except Exception as e:
            self.__logger.exception('(update-thread): thermometer error')
            GLib.idle_add(self.__receive_update, time.time(), None, e)

    def __receive_update(self, timestamp, temperature, error):
        self.__make_current(timestamp=timestamp, temperature=temperature, error=error)

    def __make_current(self, timestamp, temperature=None, error=None):
        self.__current_temperature = temperature
        if temperature is not None:
            self.__history.add(timestamp, temperature)
        self.__current_error = error
        if error is not None:
            self.__logger.error('{}'.format(error))
            self.emit_error(error)

    def _startup(self):
        self.__logger.info('starting')

        if self.__update_interval == 0:
            self.__logger.info('no background updates desired')
        else:
            try:
                temperature = self.__thermometer.get_temperature()
                self.__make_current(timestamp=time.time(), temperature=temperature, error=None)
                self.__logger.debug('startup: successfully read temperature -> {}'.format(temperature))
            except HeatingError as e:
                self.__logger.exception('startup: cannot read temperature')
                self.__make_current(timestamp=time.time(), temperature=None, error=e)

            self.__logger.info('schedule temperature updates every {} seconds'.format(self.__update_interval))
            self.__background_thread = ThreadPoolExecutor(max_workers=1)
            self.__update_timer_tag = GLib.timeout_add_seconds(self.__update_interval, self.__schedule_update)

    def _shutdown(self):
        self.__logger.info('stopping')
        if self.__update_interval != 0:
            self.__background_thread.shutdown(wait=True)
            GLib.source_remove(self.__update_timer_tag)

    def _onbus(self):
        if self.__current_error is not None:
            self.emit_error(self.__current_error)
