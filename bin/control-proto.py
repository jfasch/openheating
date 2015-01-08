#!/usr/bin/python3

from openheating.dbus.thermometer_center_client import DBusThermometerCenter
from openheating.dbus.switch_center_client import DBusSwitchCenter
from openheating.dbus.rebind import DBusConnectionProxy
from openheating.testutils.switch import TestSwitch
from openheating.switch import Switch
from openheating.sink import Sink
from openheating.passive_source import PassiveSource
from openheating.oil_combo import OilCombo
from openheating.transport import Transport
from openheating.hysteresis import Hysteresis
from openheating.thinking import Brain
from openheating.error import HeatingError

import sys
import time
from datetime import datetime

connection_proxy = DBusConnectionProxy('tcp:host=192.168.1.11,port=6666')
thermo_center = DBusThermometerCenter(connection_proxy=connection_proxy, name='org.openheating.thermometer_center', path='/thermometer_center')
switch_center = DBusSwitchCenter(connection_proxy=connection_proxy, name='org.openheating.switch_center', path='/switch_center')

sink = Sink(
    name='boiler', 
    thermometer=thermo_center.get_thermometer('boiler-top'), 
    hysteresis=Hysteresis(low=50, high=55))

# source = OilCombo(
#     name='oil',
#     enable_switch=TestSwitch(name="enable", initial_state=Switch.OPEN, output=sys.stdout),
#     burn_switch=TestSwitch(name="burn", initial_state=Switch.OPEN, output=sys.stdout),
#     thermometer=thermo_center.get_thermometer('oel-puffer'))
source = PassiveSource(name='ofen', thermometer=thermo_center.get_thermometer('ofen'))

transport = Transport(
    name='ww',
    source=source, 
    sink=sink, 
    # adapt hysteresis to something more realistic
    diff_hysteresis=Hysteresis(low=0, high=1), 
    pump_switch=TestSwitch(name="pumpe-hk", initial_state=Switch.OPEN, output=sys.stdout))

brain = Brain()
brain.add(sink)
brain.add(source)
brain.add(transport)

#source.enable()

round = 0
while True:
    brain.think(str(round))
    round += 1
    time.sleep(5)
