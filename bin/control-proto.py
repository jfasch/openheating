#!/usr/bin/python3

from openheating.dbus.thermometer_center_client import DBusThermometerCenter
from openheating.dbus.switch_center_client import DBusSwitchCenter
from openheating.dbus.rebind import DBusClientConnection
from openheating.testutils.switch import TestSwitch
from openheating.sink import Sink
from openheating.passive_source import PassiveSource
from openheating.switch_center import SwitchCenter
from openheating.oil import OilCombo
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

switch_center = DBusSwitchCenter(connection=connection, name='org.openheating.heizraum.center', path='/switches')
# switch_center = SwitchCenter(switches={
#     'pumpe-ww': TestSwitch(name='pumpe-ww', initial_state=False),
#     'pumpe-hk': TestSwitch(name='pumpe-hk', initial_state=False),
#     'oel-enable': TestSwitch(name='oel-enable', initial_state=False),
#     'oel-burn': TestSwitch(name='oel-burn', initial_state=False),
#     })

th_essraum = thermo_center.get_thermometer('essraum')
th_boiler_top = thermo_center.get_thermometer('boiler-top')
th_ofen = thermo_center.get_thermometer('ofen')
th_oil =  thermo_center.get_thermometer('oel-puffer')

sw_pumpe_ww = switch_center.get_switch('pumpe-ww')
sw_pumpe_hk = switch_center.get_switch('pumpe-hk')
sw_oil_burn = switch_center.get_switch('oel-burn')


sink_ww = Sink(
    name='boiler', 
    thermometer=th_boiler_top, 
    hysteresis=Hysteresis(low=50, high=55),
)

sink_room = Sink(
    name='room', 
    thermometer=th_essraum, 
    hysteresis=Hysteresis(low=20, high=21),
)

source_oil = OilCombo(
    name='oil',
    burn_switch=sw_oil_burn,
    thermometer=th_oil)

source_wood = PassiveSource(name='ofen', thermometer=th_ofen)

source = source_wood

transport_ww = Transport(
    name='ww',
    source=source, 
    sink=sink_ww, 
    # adapt hysteresis to something more realistic
    diff_hysteresis=Hysteresis(low=0, high=1), 
    pump_switch=sw_pumpe_ww)

transport_hk = Transport(
    name='hk',
    source=source, 
    sink=sink_room, 
    # adapt hysteresis to something more realistic
    diff_hysteresis=Hysteresis(low=0, high=1), 
    pump_switch=sw_pumpe_hk)

brain = Brain()
brain.add(sink_room)
brain.add(sink_ww)
brain.add(source)
brain.add(transport_ww)
brain.add(transport_hk)

round = 0
while True:
    brain.think(str(round))

    print('***STATES:',
          '\n* pumpe-ww:', str(sw_pumpe_ww.get_state()),
          '\n* pumpe-hk:', str(sw_pumpe_hk.get_state()),
          '\n* oel-burn:', str(sw_oil_burn.get_state()),
    )

    round += 1
    time.sleep(5)
