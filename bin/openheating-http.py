#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection

from aiohttp import web

import argparse


class ThermometerCenter:
    def __init__(self, connection):
        self.connection = connection
        self.thermometer_center = connection.get_peer(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/', 
            iface=names.IFACE.THERMOMETER_CENTER)

    async def list_simple(self, request):
        text = '<ul>'
        for name in self.thermometer_center.all_names()[0]:
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
        for name in self.thermometer_center.all_names()[0]:
            th = self.connection.get_peer(
                busname=names.BUS.THERMOMETER_SERVICE,
                path='/thermometers/'+name,
                iface=names.IFACE.THERMOMETER)
            text += '<tr><td>{description}</td><td>{name}</td><td>{temp}</td></tr>'.format(
                description=th.get_description()[0], name=th.get_name()[0], temp=th.get_temperature()[0])
        text += '</table>'
        return web.Response(content_type='text/html', text=text)


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

connection = DBusConnection(is_session=cmdline.is_session(args))
thermometer_center = ThermometerCenter(connection=connection)

app = web.Application()
app.add_routes([
    web.get('/thermometer_center/list_simple', thermometer_center.list_simple),
    web.get('/thermometer_center/list_full', thermometer_center.list_full),
])
web.run_app(app)
