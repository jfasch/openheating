from ..error import HeatingError
from .util import lifecycle as jjj_lifecycle

from pydbus import SystemBus, SessionBus

import json
import signal
import logging


def argparse_add_bus(parser):
    '''add --session|--system options to commandline parsing'''

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')

def bus_from_argparse(args):
    '''given --session|--system is in argparse, connect to the respective
    bus, and return the bus object'''

    return args.session and SessionBus() or SystemBus()


class DBusHeatingError(HeatingError):
    '''Used to pass HeatingError exceptions across the bus.

    Use @unify_error to decorate interface method implementations,
    converting native HeatingError exceptions into a DBusHeatingError.

    DBusHeatingError then collaborates with pydbus and brings the
    error across the bus:

    * on occurence (a server method throws), pydbus calls str() on it
      to build the dbus ERROR argument (dbus string).

    * at the client, when that sees a dbus ERROR, it call the
      registered class ctor on the (json) string, converting it back
      to a native DBusHeatingError. which is then thrown at the user.

    '''
    def __init__(self, details):
        if type(details) is str:
            # assume it came across the bus, so it must be json.
            details = json.loads(details)
        super().__init__(details=details)

    def __str__(self):
        '''pydbus calls str() on mapped exceptions to create the dbus ERROR
        argument. we want our heating errors to travel as json, and
        that's what we do in __str__()

        '''
        return self.to_json()

    def to_json(self):
        return json.dumps(self.details)

    @staticmethod
    def from_json(js):
        details = json.loads(js)
        return DBusHeatingError(details=details)

