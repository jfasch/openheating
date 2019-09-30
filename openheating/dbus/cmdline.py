from pydbus import SystemBus, SessionBus


def add_dbus_options(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus(args):
    return args.session and SessionBus() or SystemBus()
