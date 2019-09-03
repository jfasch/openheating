#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection
from openheating.dbus.thermometer_center import DBusThermometerCenter_Client

from aiohttp import web
from systemd.daemon import notify as sd_notify

import argparse


class ThermometerCenter:
    def __init__(self, connection):
        self.thermometer_center = DBusThermometerCenter_Client(connection)
        # we build our thermometer clients on-demand
        self.thermometers = {}

    async def list_simple(self, request):
        text = '<ul>'
        for name in self.thermometer_center.all_names():
            text += '<li>{name}</li>'.format(name=name)
        text += '</ul>'
        return web.Response(content_type='text/html', text=text)

    async def list_full(self, request):
        text = '<table>'

        text += '<tr>'
        text += '<th>Description</th>'
        text += '<th>Name</th>'
        text += '<th>Temperature</th>'
        text += '</tr>'
        for name in self.thermometer_center.all_names():
            th = self._get_thermometer(name)
            text += '<tr><td>{description}</td><td>{name}</td><td>{temp}</td></tr>'.format(
                description=th.get_description(), name=th.get_name(), temp=th.get_temperature())
        text += '</table>'
        return web.Response(content_type='text/html', text=text)

    def _get_thermometer(self, name):
        return self.thermometers.setdefault(name, self.thermometer_center.get_thermometer(name))


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
cmdline.add_dbus_options(parser)
parser.add_argument('--no-notify', action='store_true', 
                    help='Do not notify systemd of readiness (for example when started by hand during development)')
args = parser.parse_args()

connection = DBusConnection(is_session=cmdline.is_session(args))
thermometer_center = ThermometerCenter(connection=connection)

app = web.Application()
app.add_routes([
    web.get('/thermometer_center/list_simple', thermometer_center.list_simple),
    web.get('/thermometer_center/list_full', thermometer_center.list_full),
])

# notify systemd about readiness
sd_notify("READY=1")

web.run_app(app)
