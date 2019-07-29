#!/usr/bin/python3

from aiohttp import web
import ravel


bus = ravel.session_bus()
service = bus['org.openheating.ThermometerService']
object = service['/']
iface = object.get_interface('org.openheating.ThermometerService')

async def list_thermometers(request):
    text = '<ul>'
    for thermometer_name in iface.all_names()[0]:
        thobject = service['/thermometers/'+thermometer_name]
        thiface = thobject.get_interface('org.openheating.Thermometer')
        text += '<li>{name}: {temp}</li>'.format(name=thermometer_name, temp=thiface.get_temperature()[0])
    text += '</ul>'

    return web.Response(content_type='text/html', text=text)

app = web.Application()
app.router.add_get('/', list_thermometers)
web.run_app(app)
