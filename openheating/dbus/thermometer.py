from . import interface_repo
from . import node
from . import error
from . import lifecycle
from .pollable_client import Pollable_Client

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

class ThermometerPollable_Client(Pollable_Client):
    def __init__(self, bus):
        super().__init__(bus=bus, busname=names.Bus.THERMOMETERS, path='/')

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
                                               interface_repo.TEMPERATUREHISTORY,
                                               interface_repo.POLLABLE))
class Thermometer_Server:
    '''D-Bus object representing various aspects of a thermometer.

    * **Thermometer**: Current temperature, thermometer name and
      description.

    * **Temperature history**: keeps temperature values from the past,
      accessible for, for example, histogram generation, or gradient
      calculation.

    * **Polling**: a poll initiates a temperature read in the
      background; the call returns immediately. Reason: Onewire
      temperature reads take over a second, and the poller sure has
      other things to do in the meantime.

    '''
    def __init__(self, name, description, thermometer, history):
        assert isinstance(thermometer, Thermometer)

        self.__name = name
        self.__description = description
        self.__thermometer = thermometer

        self.__history = history

        self.__current_temperature = None
        self.__current_error = HeatingError('reading temperature too early, not yet initialized')

        self.__background_thread = None

        self.__logger = logging.getLogger(self.__name)

    def get_name(self):
        '''Thermometer name'''
        return self.__name

    def get_description(self):
        '''Thermometer description'''
        return self.__description

    def get_temperature(self):
        '''Current temperature'''
        if self.__current_error:
            raise self.__current_error
        return self.__current_temperature

    def force_update(self, timestamp):
        self.__make_current(timestamp=timestamp, temperature=self.__thermometer.get_temperature())

    def distill(self, granularity, duration):
        '''Extract values from temperature history

        :param granularity: minimum gap between two samples (in
                seconds or datetime.timedelta)

        :param duration: time span from now in the past (in seconds or
                         datetime.timedelta)

        '''
        return list(self.__history.distill(granularity=granularity, duration=duration))

    def poll(self, timestamp):
        '''Initiate a background temperature reading and return
        immediately. When reading completes, the temperature is added
        to the history with timestamp.

        '''
        self.__background_thread.submit(self.__update, timestamp)

    def __update(self, timestamp):
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
            GLib.idle_add(self.__receive_update, timestamp, current_temperature, None)
        except Exception as e:
            self.__logger.exception('(update-thread): thermometer error')
            GLib.idle_add(self.__receive_update, timestamp, None, e)

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

        # initial temperature read, just to have something in case
        # someone asks. this carries timestamp 0/epoch; cannot simply
        # take wall clock time here - unittests fake the time, and
        # replays bring their own (past) timestamps.

        # further temperature reads are initiated using poll() which
        # brings us the timestamp as a parameter. it's only the first
        # measurement that has epoch timestamp.
        try:
            temperature = self.__thermometer.get_temperature()
            self.__make_current(timestamp=0, temperature=temperature, error=None)
            self.__logger.debug('startup: successfully read temperature -> {}'.format(temperature))
        except HeatingError as e:
            self.__logger.exception('startup: cannot read temperature')
            self.__make_current(timestamp=0, temperature=None, error=e)

        # start background thread to perform future temperature reads.
        self.__background_thread = ThreadPoolExecutor(max_workers=1)

    def _shutdown(self):
        self.__logger.info('stopping')
        self.__background_thread.shutdown(wait=True)

    def _onbus(self):
        if self.__current_error is not None:
            self.emit_error(self.__current_error)
