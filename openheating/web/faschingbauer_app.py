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

    def thermometer_names(self):
        return list(self.thermometers.keys())

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
            menu.Entry(
                url=flask.url_for('home'),
                image_url=flask.url_for('static', filename='icons/www.opensecurityarchitecture.org/osa_home.svg'),
                alt='Home',
            ),
            menu.Entry(
                url=flask.url_for('thermometers'),
                image_url=flask.url_for('static', filename='icons/www.opensecurityarchitecture.org/osa_ics_thermometer.svg'),
                alt='Thermometers',
            ),
            menu.Entry(
                url=flask.url_for('errors'),
                image_url=flask.url_for('static', filename='icons/www.opensecurityarchitecture.org/osa_warning.svg'),
                alt='Errors',
            ),
        ))
        return flask.render_template(
            template,
            app = self,
            menu = fmenu,
            **kwargs)