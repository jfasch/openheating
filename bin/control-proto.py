#!/usr/bin/python3

from openheating.dbus.thermometer_center_client import DBusThermometerCenter
from openheating.dbus.switch_center_client import DBusSwitchCenter
from openheating.dbus.rebind import DBusClientConnection
from openheating.testutils.switch import TestSwitch
from openheating.sink import Sink
from openheating.passive_source import PassiveSource
from openheating.switch_center import SwitchCenter
from openheating.oil_combo import OilCombo
from openheating.transport import Transport
from openheating.hysteresis import Hysteresis
from openheating.thinking import Brain
from openheating.error import HeatingError

import logging
import sys
import time
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

connection = DBusClientConnection('tcp:host=192.168.1.11,port=6666')
thermo_center = DBusThermometerCenter(connection=connection, name='org.openheating.heizraum.center', path='/thermometers')

# switch_center = DBusSwitchCenter(connection=connection, name='org.openheating.heizraum.center', path='/switches')
switch_center = SwitchCenter(switches={
    'pumpe-ww': TestSwitch(name='pumpe-ww', initial_state=False, output=sys.stdout),
    'oel-enable': TestSwitch(name='oel-enable', initial_state=False, output=sys.stdout),
    'oel-burn': TestSwitch(name='oel-burn', initial_state=False, output=sys.stdout),
    })

th_boiler_top = thermo_center.get_thermometer('boiler-top')
th_ofen = thermo_center.get_thermometer('ofen')
th_oil =  thermo_center.get_thermometer('oel-puffer')

sw_pumpe_ww = switch_center.get_switch('pumpe-ww')
sw_oil_enable = switch_center.get_switch('oel-enable')
sw_oil_burn = switch_center.get_switch('oel-burn')


sink = Sink(
    name='boiler', 
    thermometer=th_boiler_top, 
    hysteresis=Hysteresis(low=50, high=55),
#    hysteresis=Hysteresis(low=20, high=30),
)

source = OilCombo(
    name='oil',
    enable_switch=sw_oil_enable,
    burn_switch=sw_oil_burn,
    thermometer=th_oil)
source.enable()

# source = PassiveSource(name='ofen', thermometer=th_ofen)

transport = Transport(
    name='ww',
    source=source, 
    sink=sink, 
    # adapt hysteresis to something more realistic
    diff_hysteresis=Hysteresis(low=0, high=1), 
    pump_switch=sw_pumpe_ww)

brain = Brain()
brain.add(sink)
brain.add(source)
brain.add(transport)

round = 0
while True:
    brain.think(str(round))

    print('***STATES:',
          '\n* pumpe-ww:', str(sw_pumpe_ww.get_state()),
          '\n* oel-enable:', str(sw_oil_enable.get_state()),
          '\n* oel-burn:', str(sw_oil_burn.get_state()),
    )

    round += 1
    time.sleep(5)
