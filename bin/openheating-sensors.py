#!/usr/bin/python3

from openheating.hardware.sensors_config import SensorsConfig

from argparse import ArgumentParser
import logging
import logging.handlers


parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--syslog', action='store_true', default=False, help='Log to syslog')
args = parser.parse_args()

if args.syslog:
    h = logging.handlers.SysLogHandler(address='/dev/log')
else:
    h = logging.StreamHandler()
logging.getLogger().addHandler(h)

try:
    config = SensorsConfig(open(args.config_file).read())
    for s in config.sensors():
        s.temperature()
except Exception as e:
    logging.exception(str(e))
