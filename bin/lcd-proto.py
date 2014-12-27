#!/usr/bin/python3

from openheating.hd44780 import HD44780_LCD
from openheating.dbus.thermometer import DBusThermometer

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


while True:
    temps = {
        'now': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'boiler-top': boiler_top.temperature(),
        'boiler-middle': boiler_middle.temperature(),
        'boiler-bottom': boiler_bottom.temperature(),
        'hk-vl': hk_vl.temperature(),
        'boiler-vl': boiler_vl.temperature(),
        'ofen-vl': ofen_vl.temperature(),
        'ofen': ofen.temperature(),
        }
    msg = \
        ('%(now)s\n' + \
         'Boi:%(boiler-top).1f/%(boiler-middle).1f/%(boiler-bottom).1f\n' + \
         'HK:%(hk-vl).1f,WW:%(boiler-vl).1f\n' + \
         'Ofen:%(ofen).1f,VL:%(ofen-vl).1f') % temps

    print(msg+'\n--')

    display.clear()
    display.message(msg)
    time.sleep(15)
