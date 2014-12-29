#!/usr/bin/python3

from openheating.hd44780 import HD44780_LCD
from openheating.dbus.thermometer import DBusThermometer
from openheating.error import HeatingException

import dbus.bus
import time
from datetime import datetime

connection = dbus.bus.BusConnection('tcp:host=192.168.1.11,port=6666')
display = HD44780_LCD(
    rs=27,
    en=22,
    d4=25,
    d5=24,
    d6=23,
    d7=18, 
    cols=20,
    lines=4)

boiler_top = DBusThermometer(connection=connection, name='org.openheating.boiler', path='/thermometers/top')
boiler_middle = DBusThermometer(connection=connection, name='org.openheating.boiler', path='/thermometers/middle')
boiler_bottom = DBusThermometer(connection=connection, name='org.openheating.boiler', path='/thermometers/bottom')
hk_vl = DBusThermometer(connection=connection, name='org.openheating.heizraum', path='/thermometers/heizkreis_vl')
boiler_vl = DBusThermometer(connection=connection, name='org.openheating.heizraum', path='/thermometers/boiler_vl')
ofen_vl = DBusThermometer(connection=connection, name='org.openheating.heizraum', path='/thermometers/ofen_vl')
ofen = DBusThermometer(connection=connection, name='org.openheating.ofen', path='/thermometers/ofen')

def get_temperature(thermometer):
    try:
        return '%.1f' % thermometer.temperature()
    except HeatingException:
        return 'ERR!'

while True:
    temps = {
        'now': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'boiler-top': get_temperature(boiler_top),
        'boiler-middle': get_temperature(boiler_middle),
        'boiler-bottom': get_temperature(boiler_bottom),
        'hk-vl': get_temperature(hk_vl),
        'boiler-vl': get_temperature(boiler_vl),
        'ofen-vl': get_temperature(ofen_vl),
        'ofen': get_temperature(ofen),
        }
    msg = \
        ('%(now)s\n' + \
         'Boi:%(boiler-top)s/%(boiler-middle)s/%(boiler-bottom)s\n' + \
         'HK:%(hk-vl)s,WW:%(boiler-vl)s\n' + \
         'Ofen:%(ofen)s,VL:%(ofen-vl)s') % temps

    print(msg+'\n--')

    display.clear()
    display.message(msg)
    time.sleep(15)
