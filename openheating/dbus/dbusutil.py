from pydbus import SystemBus, SessionBus


BUS_KIND_SESSION = 7
BUS_KIND_SYSTEM = 42

def argparse_add_bus(parser):
    '''add --session|--system options to commandline parsing'''

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus_from_argparse(args):
    '''given --session|--system is in argparse, connect to the respective
    bus, and return the bus object'''

    return args.session and SessionBus() or SystemBus()

def buskind_from_argparse(args):
    return args.session and BUS_KIND_SESSION or BUS_KIND_SYSTEM
