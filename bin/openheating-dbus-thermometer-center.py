#!/usr/bin/python3

from openheating.dbus.thermometer_center_object import DBusThermometerCenterObject
from openheating.dbus.thermometer_center_config import ThermometerCenterConfig
from openheating.dbus.service_combo import DBusServiceCombo
from openheating.dbus.rebind import DBusConnectionProxy
from openheating.thermometer_center import ThermometerCenter

from argparse import ArgumentParser
import logging
import logging.handlers


parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--pid-file', type=str, help='PID file (to be documented)')
parser.add_argument('--syslog', action='store_true', default=False, help='PID file (to be documented)')
args = parser.parse_args()

if args.syslog:
    h = logging.handlers.SysLogHandler(address='/dev/log')
    logging.getLogger().addHandler(h)

config = ThermometerCenterConfig(open(args.config_file).read())
center = ThermometerCenter(
    ((name, creator.create(DBusConnectionProxy(config.daemon_address()))) for name, creator in config.iter_thermometers()))

class MyCombo(DBusServiceCombo):
    def __init__(self, pidfile, config):
        DBusServiceCombo.__init__(self, pidfile=pidfile, daemon_address=config.daemon_address(), busname=config.bus_name())
    def create_objects(self, connection):
        DBusThermometerCenterObject(connection=connection, object_path=config.path(), center=center)

combo = MyCombo(pidfile=args.pid_file, config=config)
combo.run()
