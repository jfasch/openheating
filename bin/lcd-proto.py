#!/usr/bin/python3

from openheating.logic.thermometer_center import ThermometerCenterThermometer
from openheating.dbus.client_thermometer_center import DBusThermometerCenterClient
from openheating.dbus.connection import DBusClientConnection
from openheating.hardware.hd44780 import HD44780_LCD
from openheating.base.error import HeatingError

import time
from datetime import datetime

connection = DBusClientConnection('tcp:host=192.168.1.11,port=6666')
display = HD44780_LCD(
    rs=27,
    en=22,
    d4=25,
    d5=24,
    d6=23,
    d7=18, 
    cols=20,
    lines=4)

thermo_center = DBusThermometerCenterClient(
    connection=connection,
    name='org.openheating.heizraum.center',
    path='/thermometers')

boiler_top = ThermometerCenterThermometer(center=thermo_center, name='boiler-top')
boiler_middle = ThermometerCenterThermometer(center=thermo_center, name='boiler-middle')
boiler_bottom = ThermometerCenterThermometer(center=thermo_center, name='boiler-bottom')
hk_vl = ThermometerCenterThermometer(center=thermo_center, name='hk-vl')
boiler_vl = ThermometerCenterThermometer(center=thermo_center, name='boiler-vl')
ofen_vl = ThermometerCenterThermometer(center=thermo_center, name='ofen-vl')
ofen = ThermometerCenterThermometer(center=thermo_center, name='ofen')
oel_puffer = ThermometerCenterThermometer(center=thermo_center, name='oel-puffer')
essraum = ThermometerCenterThermometer(center=thermo_center, name='essraum')

def get_temperature(thermometer, places):
    try:
        return ('%.'+str(places)+'f') % thermometer.temperature()
    except HeatingError:
        return 'ERR!'

while True:
    temps = {
        'now': str(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')),
        'essraum': get_temperature(essraum, 1),
        'boiler-top': get_temperature(boiler_top, 0),
        'boiler-middle': get_temperature(boiler_middle, 0),
        'boiler-bottom': get_temperature(boiler_bottom, 0),
        'hk-vl': get_temperature(hk_vl, 1),
        'boiler-vl': get_temperature(boiler_vl, 1),
        'ofen-vl': get_temperature(ofen_vl, 1),
        'ofen': get_temperature(ofen, 1),
        'oel-puffer': get_temperature(oel_puffer, 1),
        }
    msg = \
        ('%(now)s\n' + \
         'E:%(essraum)s    B:%(boiler-top)s/%(boiler-middle)s/%(boiler-bottom)s\n' + \
         'O:%(oel-puffer)s   H:%(ofen)s/%(ofen-vl)s\n' + \
         'HK:%(hk-vl)s      WW:%(boiler-vl)s'
         ) % temps

    print(msg+'\n--')

    display.clear()
    display.message(msg)
    time.sleep(15)
