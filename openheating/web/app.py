from openheating.dbus.thermometer_center import ThermometerCenter_Client

import flask

import sys
import datetime


class App:
    def __init__(self, 
                 flask_template_folder,
                 dbus_connection):

        self.__app = flask.Flask(
            import_name = 'openheating',
            template_folder = flask_template_folder,
        )
        self.__app.add_url_rule('/', view_func=self.__view_home)
        self.__app.add_url_rule('/thermometers', view_func=self.__view_thermometers)
        self.__app.add_url_rule('/thermometers/<name>', view_func=self.__view_thermometer)

        self.__thermometer_center_client = ThermometerCenter_Client(dbus_connection)
        self.__thermometers = {}
        self.__thermometer_histories = {}
        for name in self.__thermometer_center_client.all_names():
            self.__thermometers[name] = self.__thermometer_center_client.get_thermometer(name)
            self.__thermometer_histories[name] = self.__thermometer_center_client.get_history(name)

    def run(self, *args, **kwargs):
        self.__app.run(*args, **kwargs)

    def __render_template(self, template, **kwargs):
        menu =  [
            (flask.url_for('__view_home'), 'Home'),
            (flask.url_for('__view_thermometers'), 'Thermometers'),
        ]
        return flask.render_template(
            template,
            menu = menu,
            **kwargs)

    def __view_home(self):
        return self.__render_template(
            'home.html',
        )
        
    def __view_thermometers(self):
        thermometer_urls = { name: flask.url_for('__view_thermometer', name=name) for name in self.__thermometers.keys() }
        return self.__render_template(
            'thermometers.html', 
            thermometers = self.__thermometers.values(),
            thermometer_urls = thermometer_urls,
        )

    def __view_thermometer(self, name):
        thermometer = self.__thermometers[name]
        history = self.__thermometer_histories[name]
        
        samples = []
        for timestamp, temperature in history.all():
            samples.append((str(datetime.datetime.fromtimestamp(timestamp)), temperature))

        return self.__render_template(
            'thermometer.html',
            thermometer = thermometer,
            samples = samples,
        )
