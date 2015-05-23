#!/usr/bin/python3

from openheating.dbus.client_thermometer_center import DBusThermometerCenterClient
from openheating.dbus.client_switch_center import DBusSwitchCenterClient
from openheating.dbus.connection import DBusClientConnection
from openheating.logic.thinking import Brain
from openheating.logicjf_control import JFControl

import logging
import sys
import time
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

#dbus_address = 'tcp:host=192.168.1.11,port=6666'
dbus_address = 'unix:path=/tmp/openheating-simulation/openheating-dbus-daemon.socket'

connection = DBusClientConnection(dbus_address)

switch_center = DBusSwitchCenterClient(connection=connection, name='org.openheating.heizraum.center', path='/switches')
thermometer_center = DBusThermometerCenterClient(connection=connection, name='org.openheating.heizraum.center', path='/thermometers')

brain = Brain()

jf = JFControl(
    switch_center = switch_center,
    thermometer_center = thermometer_center,

    th_room = 'essraum',
    th_water = 'boiler-top',
    th_wood = 'ofen',
    th_oil = 'oel-puffer',
    sw_water = 'pumpe-ww',
    sw_room = 'pumpe-hk',
    sw_oil = 'oel-burn',
    sw_wood_valve = 'wood-valve',
)

jf.register_thinking(brain)

round = 0
while True:
    brain.think(str(round))

    print('***STATES:',
          '\n* pumpe-ww:', str(switch_center.get_state('pumpe-ww')),
          '\n* pumpe-hk:', str(switch_center.get_state('pumpe-hk')),
          '\n* oel-burn:', str(switch_center.get_state('oel-burn')),
          '\n* wood-valve:', str(switch_center.get_state('wood-valve')),
    )

    round += 1
    time.sleep(5)
