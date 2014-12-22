#!/usr/bin/python3

from openheating.hd44780 import HD44780_LCD

import dbus.bus
import time

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

while True:
    temps = {
        'boiler-top': float(connection.get_object('org.openheating.boiler', '/thermometers/top').temperature()),
        'boiler-middle': float(connection.get_object('org.openheating.boiler', '/thermometers/middle').temperature()),
        'boiler-bottom': float(connection.get_object('org.openheating.boiler', '/thermometers/bottom').temperature()),
        'hk-vl': float(connection.get_object('org.openheating.heizraum', '/thermometers/heizkreis_vl').temperature()),
        'boiler-vl': float(connection.get_object('org.openheating.heizraum', '/thermometers/boiler_vl').temperature()),
        'ofen-vl': float(connection.get_object('org.openheating.heizraum', '/thermometers/ofen_vl').temperature()),
        }
    msg = \
        ('Boi:%(boiler-top).1f/%(boiler-middle).1f/%(boiler-bottom).1f\n' + \
        'HK:%(hk-vl).1f,WW:%(boiler-vl).1f\n' + \
        'Ofen-VL:%(ofen-vl).1f') % temps

    print(msg+'\n--')

    display.clear()
    display.message(msg)
    time.sleep(15)
