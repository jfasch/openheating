#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config import PlantConfig
from openheating.plant.service import MainService
from openheating.plant.plant import Plant
from openheating.dbus import names
from openheating.testutils import testutils

from gi.repository import GLib

import argparse
import sys
import os.path
import signal
import logging


parser = argparse.ArgumentParser(description='OpenHeating: run a plant manually (for testing and simulating)')
parser.add_argument('--config', help='Configuration file')
parser.add_argument('--simulation-dir', metavar='DIR', 
                    help='Create switch and thermometer files in DIR/switches and DIR/thermometers, respectively. '
                    'The subdirectory names are passed directly to the switch and thermometer services')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(
    args,
    # not being a dbus object, we simply identify as argv[0]
    componentname=os.path.basename(sys.argv[0]))

loop = GLib.MainLoop()
buskind = dbusutil.buskind_from_argparse(args)
bus = dbusutil.bus_from_argparse(args)

plant_config = PlantConfig()
plant_config.parse(args.config)
plant_config.add_service(MainService(config=args.config))

the_plant = Plant(services=plant_config.get_services())

try:
    the_plant.startup(
        find_exe=testutils.find_executable, # fix that somehow
        bus_kind=buskind,
        common_args=[], # could use that to pass common debug and log
                        # settings in
        capture_stderr=False, # let stderr through
    )

    signal.pthread_sigmask(signal.SIG_BLOCK, (signal.SIGINT, signal.SIGTERM))
    while True:
        sig = signal.sigwait((signal.SIGINT, signal.SIGTERM))
        if sig in (signal.SIGINT, signal.SIGTERM):
            break
        logging.error('wakeup for nothing?')
finally:
    logging.info('shutting down')
    the_plant.shutdown()
