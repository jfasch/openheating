#!/usr/bin/python3

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


try:
    from openheating.dbus.service import DBusService
    from openheating.dbus.service_config import DBusServiceConfig
    from openheating.dbus.service_combo import DBusServiceCombo
    from openheating.dbus.rebind import DBusServerConnection
    
    class MyCombo(DBusServiceCombo):
        def __init__(self, pidfile, service):
            self.__service = service
            DBusServiceCombo.__init__(self, pidfile=pidfile, daemon_address=config.daemon_address(), busname=config.bus_name())
        def create_objects(self, connection):
            self.__service.create_dbus_objects(connection=DBusServerConnection(connection=connection))

    config = DBusServiceConfig(open(args.config_file).read())
    service = DBusService(creators=config.creators())
    combo = MyCombo(pidfile=args.pid_file, service=service)
    combo.run()

except Exception as e:
    logging.exception(str(e))
