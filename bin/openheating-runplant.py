#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config_plant import PlantConfig
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
                    help='Create switch and thermometer files in subdirectories of DIR')
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

# add "main" service on top of what's there
plant_config.add_service(MainService(config=args.config))

the_plant = Plant(services=plant_config.get_services())
if args.simulation_dir is not None:
    thermometer_dir, switch_dir = the_plant.enable_simulation_mode(args.simulation_dir)
    print('starting in simulation mode:', file=sys.stderr)
    print('    thermometers in ', thermometer_dir, file=sys.stderr)
    print('    switches     in ', switch_dir, file=sys.stderr)


try:
    the_plant.startup(
        find_exe = testutils.find_executable, # fix that somehow
        bus_kind = buskind,
        common_args = logutil.get_log_config_from_argparse(args),
        capture_stderr = False, # let stderr through
    )

    signal.pthread_sigmask(signal.SIG_BLOCK, (signal.SIGINT, signal.SIGTERM, signal.SIGCHLD))
    while True:
        sig = signal.sigwait((signal.SIGINT, signal.SIGTERM, signal.SIGCHLD))
        if sig in (signal.SIGINT, signal.SIGTERM):
            break
        if sig == signal.SIGCHLD:
            logging.error('child process died')
            break
        logging.error('wakeup for nothing?')
finally:
    logging.info('shutting down')
    the_plant.shutdown()
