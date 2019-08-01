#!/usr/bin/python3

from openheating.switches_ini import read_file as read_config_file
import openheating.dbus.names as busnames
import openheating.dbus.service as dbus_service
from openheating.dbus.switch import DBusSwitch
from openheating.dbus.switch_service import DBusSwitchService

import asyncio
import argparse


def create_service(loop, switches):
    """Create the switch service

    Creates a dbus connection, and registers objects on it:

    * Switch service object
    * A switch object for each switch in `switches`

    """

    connection = dbus_service.create_connection(
        busname=busnames.switch_service_busname,
        is_session=args.session, 
        loop=loop)

    connection.register(
        path='/',
        fallback=True,
        interface=DBusSwitchService(switches=switches)
    )
    for name, switch in switches.items():
        connection.register(
            path='/switches/'+name,
            fallback=True,
            interface=DBusSwitch(switch=switch)
        )
    
    return connection

parser = argparse.ArgumentParser(description='OpenHeating: DBus switch service')
parser.add_argument('--configfile', help='Switch configuration file')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--session', action='store_true', help='Connect to the session bus')
group.add_argument('--system', action='store_true', help='Connect to the system bus')
args = parser.parse_args()

switches = read_config_file(args.configfile)

loop = asyncio.get_event_loop()
create_service(loop=loop, switches=switches)
loop.run_until_complete(dbus_service.graceful_termination(loop))
