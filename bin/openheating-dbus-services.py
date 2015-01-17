#!/usr/bin/python3

from argparse import ArgumentParser
import logging
import logging.handlers
import signal

parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--pid-file', type=str, help='PID file (to be documented)')
parser.add_argument('--syslog', action='store_true', default=False, help='PID file (to be documented)')
args = parser.parse_args()

if args.syslog:
    h = logging.handlers.SysLogHandler(address='/dev/log')
    logging.getLogger().addHandler(h)

def terminate(signum, frame):
    global running
    running = False

running = True
services = []

try:
    from openheating.dbus.service_config import DBusServicesConfig

    config = DBusServicesConfig(open(args.config_file).read())
    services = config.services()

    for s in services:
        s.start()

    print('pause')
    while running:
        try:
            signal.pause()
        except KeyboardInterrupt:
            running = False
        except OSError as e:
            if e.errno == errno.EINTR:
                continue

    for s in services:
        s.stop()

except Exception as e:
    logging.exception(str(e))
