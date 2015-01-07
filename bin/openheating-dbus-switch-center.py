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
    from openheating.dbus.switch_center_object import DBusSwitchCenterObject
    from openheating.dbus.switch_center_config import SwitchCenterConfig
    from openheating.dbus.service_combo import DBusServiceCombo
    from openheating.dbus.rebind import DBusConnectionProxy
    from openheating.switch_center import SwitchCenter
    
    config = SwitchCenterConfig(open(args.config_file).read())
    center = SwitchCenter(
        ((name, creator.create(DBusConnectionProxy(config.daemon_address()))) for name, creator in config.iter_switches()))
    
    class MyCombo(DBusServiceCombo):
        def __init__(self, pidfile, config):
            DBusServiceCombo.__init__(self, pidfile=pidfile, daemon_address=config.daemon_address(), busname=config.bus_name())
        def create_objects(self, connection):
            DBusSwitchCenterObject(connection=connection, object_path=config.path(), center=center)
    
    combo = MyCombo(pidfile=args.pid_file, config=config)
    combo.run()

except Exception as e:
    logging.exception(str(e))
