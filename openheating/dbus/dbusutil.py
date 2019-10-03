import signal


from pydbus import SystemBus, SessionBus


def argparse_add_bus(parser):
    '''add --session|--system options to commandline parsing'''

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus_from_argparse(args):
    '''given --session|--system is in argparse, connect to the respective
    bus, and return the bus object'''

    return args.session and SessionBus() or SystemBus()

def graceful_termination(loop):
    '''install the appropriate signal handler, and take care to terminate
    the eventloop gracefully'''

    def quit(signal, frame):
        loop.quit()
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    signal.signal(signal.SIGQUIT, quit)
