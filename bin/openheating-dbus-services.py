#!/usr/bin/python3

from openheating.base import logger 

from argparse import ArgumentParser
import signal
import os

parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--pid-file', type=str, help='PID file (to be documented)')
parser.add_argument('--print-pid', action='store_true', default=False, help='print PID to stdout')
parser.add_argument('--syslog', action='store_true', default=False, help='Log to syslog')
parser.add_argument('--verbose', action='store_true', default=False, help='print debug output')
args = parser.parse_args()

logger.init(name='main', syslog=args.syslog, verbose=args.verbose)

def terminate(signum, frame):
    global running
    running = False

running = True
services = []

try:
    from openheating.dbus.service_config import DBusServicesConfig

    config = DBusServicesConfig(open(args.config_file).read())
    services = config.services()

    if args.pid_file is not None:
        pf = open(args.pid_file, 'w')
        pf.write(str(os.getpid())+'\n')
        pf.close()

    if args.print_pid:
        print(os.getpid())


    for s in services:
        s.start()

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGQUIT, terminate)
    signal.signal(signal.SIGINT, terminate)

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

    if args.pid_file is not None:
        os.remove(args.pid_file)

except Exception as e:
    logger.exception(str(e))
