#!/usr/bin/python3

from openheating.dbus.thermometer_center_client import DBusThermometerCenter
from openheating.dbus.switch_center_client import DBusSwitchCenter
from openheating.dbus.rebind import DBusClientConnection
from openheating.thinking import Brain
from openheating.jf_control import JFControl

import logging
import sys
import time
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

#dbus_address = 'tcp:host=192.168.1.11,port=6666'
dbus_address = 'unix:path=/tmp/openheating-simulation/openheating-dbus-daemon.socket'

connection = DBusClientConnection(dbus_address)

switch_center = DBusSwitchCenter(connection=connection, name='org.openheating.heizraum.center', path='/switches')
thermometer_center = DBusThermometerCenter(connection=connection, name='org.openheating.heizraum.center', path='/thermometers')

brain = Brain()

jf = JFControl(switch_center=switch_center,
               thermometer_center=thermometer_center)
jf.register_thinking(brain)

# enter polling loop. gather switches for diagnostic output.
pumpe_ww = switch_center.get_switch('pumpe-ww')
pumpe_hk = switch_center.get_switch('pumpe-hk')
oil_burn = switch_center.get_switch('oel-burn')
wood_valve = switch_center.get_switch('wood-valve')

round = 0
while True:
    brain.think(str(round))

    print('***STATES:',
          '\n* pumpe-ww:', str(pumpe_ww.get_state()),
          '\n* pumpe-hk:', str(pumpe_hk.get_state()),
          '\n* oel-burn:', str(oil_burn.get_state()),
          '\n* wood-valve:', str(wood_valve.get_state()),
    )

    round += 1
    time.sleep(5)
