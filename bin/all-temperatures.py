#!/usr/bin/python3

from openheating.dbus.thermometer_center_client import DBusThermometerCenter
from openheating.dbus.rebind import DBusClientConnection
from openheating.error import HeatingError

from datetime import datetime
import time

def make_temperature(center, name):
    try:
        return '%.1f' % center.temperature(name)
    except HeatingError as e:
        return 'Error: '+str(e)

connection = DBusClientConnection('tcp:host=192.168.1.11,port=6666')
thermo_center = DBusThermometerCenter(connection=connection, name='org.openheating.heizraum.center', path='/thermometers')

all_names = sorted(thermo_center.all_names())

while True:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for name in all_names:
        print('    %s: %s' % (name, make_temperature(thermo_center, name)))
    time.sleep(5)

