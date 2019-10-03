from . import names
from ..thermometer import Thermometer
from ..error import HeatingError
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


class Thermometer_Server:
    dbus = """
    <node>
      <interface name='{thermometer_iface}'>
        <method name='get_name'>
          <arg type='s' name='response' direction='out'/>
        </method>
        <method name='get_description'>
          <arg type='s' name='response' direction='out'/>
        </method>
        <method name='get_temperature'>
          <arg type='d' name='response' direction='out'/>
        </method>
      </interface>
    </node>
    """.format(thermometer_iface=names.IFACE.THERMOMETER)

    def __init__(self, update_interval, thermometer, history):
        assert isinstance(thermometer, Thermometer)

        # trusting the GIL, we don't lock these against the update
        # background thread (though we probably should anyway).
        self.__thermometer = thermometer
        self.__history = history

        # initialize current temperature value before starting to
        # periodically update it. we do this because once the main
        # event loop is started and dbus calls come in we want to have
        # a value available.

        self.__current_temperature = self.__thermometer.get_temperature()

        # schedule periodic temperature updates in a *background
        # thread*. this is because w1 bitbanging blocks for almost a
        # second per temperature read.

        logger.info('{}: schedule temperature updates every {} seconds'.format(self.__thermometer.get_name(), update_interval))
        self.__background_thread = ThreadPoolExecutor(max_workers=1)
        GLib.timeout_add_seconds(update_interval, self.__schedule_update)

    def get_name(self):
        return self.__thermometer.get_name()

    def get_description(self):
        return self.__thermometer.get_description()

    def get_temperature(self):
        return self.__current_temperature

    def __schedule_update(self):
        # submit work to the background thread, *not* waiting for the
        # returned future object (alas, we don't want to block)
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
        
        current_temperature = self.__thermometer.get_temperature()
        GLib.idle_add(self.__receive_update, current_temperature)
        
        logger.debug('{} (update-thread): sensor has {} degrees; pushing into main loop'.format(
            self.__thermometer.get_name(), current_temperature))

    def __receive_update(self, current_temperature):
        logger.debug('{}: receiving {} degrees from update-thread'.format(self.__thermometer.get_name(), current_temperature))
        self.__current_temperature = current_temperature
        self.__history.add(time.time(), current_temperature)
