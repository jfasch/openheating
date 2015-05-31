#!/usr/bin/python3

ADDRESS = 'unix:path=/tmp/openheating-simulation/openheating-dbus-daemon.socket'
THERMOMETER_CENTER_NAME = 'at.co.faschingbauer.center'
THERMOMETER_CENTER_PATH = '/thermometers'

from openheating.logic.lcd import LCD
from openheating.dbus.client_thermometer_center import DBusThermometerCenterClient
from openheating.logic.brain import Brain
from openheating.dbus.connection import DBusClientConnection

import time


brain = Brain([
    LCD(name='lcd',
        thermometer_center = DBusThermometerCenterClient(
            connection=DBusClientConnection(ADDRESS),
            name=THERMOMETER_CENTER_NAME,
            path=THERMOMETER_CENTER_PATH),
        
        boiler_top='boiler-top',
        boiler_middle='boiler-middle',
        boiler_bottom='boiler-bottom',
        hk_vl='hk-vl',
        boiler_vl='boiler-vl',
        ofen_vl='ofen-vl',
        ofen='ofen',
        oel_puffer='oel-puffer',
        essraum='essraum',

        simulation=True)
])

while True:
    brain.think()
    time.sleep(15)
