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
    from openheating.dbus.switch_object import DBusSwitchObject
    from openheating.dbus.switch_service_config import SwitchServiceConfig
    from openheating.dbus.service_combo import DBusServiceCombo

    config = SwitchServiceConfig(open(args.config_file).read())

    class MyCombo(DBusServiceCombo):
        def __init__(self, pidfile, config):
            DBusServiceCombo.__init__(self, pidfile, config.daemon_address(), config.bus_name())
            self.__switches = config.switches()
        def create_objects(self, connection):
            for t in self.__switches:
                ctor_params = { 'connection': connection }
                ctor_params.update(t)
                DBusSwitchObject(**ctor_params)
    
    combo = MyCombo(pidfile=args.pid_file, config=config)
    combo.run()

except Exception as e:
    logging.exception(str(e))
