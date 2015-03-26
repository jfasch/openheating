#!/usr/bin/python3

from openheating.dbus.client_thermometer_center import DBusThermometerCenterClient
from openheating.dbus.client_switch_center import DBusSwitchCenterClient
from openheating.dbus.connection import DBusClientConnection
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

switch_center = DBusSwitchCenterClient(connection=connection, name='org.openheating.heizraum.center', path='/switches')
thermometer_center = DBusThermometerCenterClient(connection=connection, name='org.openheating.heizraum.center', path='/thermometers')

th_essraum = thermometer_center.get_thermometer('essraum')
th_boiler_top = thermometer_center.get_thermometer('boiler-top')
th_ofen = thermometer_center.get_thermometer('ofen')
th_oil = thermometer_center.get_thermometer('oel-puffer')
sw_pumpe_ww = switch_center.get_switch('pumpe-ww')
sw_pumpe_hk = switch_center.get_switch('pumpe-hk')
sw_oil_burn = switch_center.get_switch('oel-burn')
sw_wood_valve = switch_center.get_switch('wood-valve')

brain = Brain()

jf = JFControl(
    th_essraum = th_essraum,
    th_boiler_top = th_boiler_top,
    th_ofen = th_ofen,
    th_oil = th_oil,
    sw_pumpe_ww = sw_pumpe_ww,
    sw_pumpe_hk = sw_pumpe_hk,
    sw_oil_burn = sw_oil_burn,
    sw_wood_valve = sw_wood_valve,
)

jf.register_thinking(brain)

round = 0
while True:
    brain.think(str(round))

    print('***STATES:',
          '\n* pumpe-ww:', str(sw_pumpe_ww.get_state()),
          '\n* pumpe-hk:', str(sw_pumpe_hk.get_state()),
          '\n* oel-burn:', str(sw_oil_burn.get_state()),
          '\n* wood-valve:', str(sw_wood_valve.get_state()),
    )

    round += 1
    time.sleep(5)
