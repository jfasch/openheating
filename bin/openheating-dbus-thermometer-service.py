#!/usr/bin/python3

from openheating.dbus.thermometer_object import DBusThermometerObject
from openheating.dbus.thermometer_service_config import ThermometerDBusServiceConfigParser
from openheating.dbus.service_combo import DBusServiceCombo

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

config = ThermometerDBusServiceConfigParser().parse(open(args.config_file).read())

class MyCombo(DBusServiceCombo):
    def __init__(self, pidfile, config):
        DBusServiceCombo.__init__(self, pidfile, config.daemon_address(), config.bus_name())
        self.__thermometers = config.thermometers()
    def create_objects(self, connection):
        for t in self.__thermometers:
            ctor_params = { 'connection': connection }
            ctor_params.update(t)
            DBusThermometerObject(**ctor_params)

combo = MyCombo(pidfile=args.pid_file, config=config)
combo.run()
