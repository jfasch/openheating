from . import menu

from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.errors import Errors_Client

import flask


class FaschingbauerApp:
    def __init__(self,
                 flask_args,
                 dbus_connection):

        self.flask = flask.Flask(import_name = 'openheating', **flask_args)

        self.thermometer_center_client = ThermometerCenter_Client(dbus_connection)
        self.thermometers = {}
        self.thermometer_histories = {}
        for name in self.thermometer_center_client.all_names():
            self.thermometers[name] = self.thermometer_center_client.get_thermometer(name)
            self.thermometer_histories[name] = self.thermometer_center_client.get_history(name)
        self.errors_client = Errors_Client(dbus_connection)

    def setup(self):
        from . import faschingbauer_home
        from . import svg
        from . import thermometers
        from . import thermometer
        from . import errors

    def run(self, *args, **kwargs):
        self.flask.run(*args, **kwargs)

    def render_template(self, template, **kwargs):
        fmenu = menu.Menu(entries=(
            menu.Entry(altname='Home', url=flask.url_for('home')),
            menu.Entry(altname='Thermometers', url=flask.url_for('thermometers')),
            menu.Entry(altname='Errors', url=flask.url_for('errors')),
        ))
        return flask.render_template(
            template,
            app = self,
            menu = fmenu,
            **kwargs)
