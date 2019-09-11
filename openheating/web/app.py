from openheating.dbus.thermometer_center import ThermometerCenter_Client

import flask


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

        self.__thermometer_center_client = ThermometerCenter_Client(dbus_connection)
        self.__thermometers = {}
        for name in self.__thermometer_center_client.all_names():
            self.__thermometers[name] = self.__thermometer_center_client.get_thermometer(name)

        self.__menu = [
            ('/thermometers', 'Thermometers'),
            ('/dummy', 'Dummy'),
        ]

    def run(self, *args, **kwargs):
        self.__app.run(*args, **kwargs)

    def __common_args(self):
        return {
            'menu': self.__menu,
            'remote_addr': flask.request.remote_addr,
        }

    def __view_home(self):
        return flask.render_template(
            'home.html', 
            **self.__common_args(),
        )
        
    def __view_thermometers(self):
        return flask.render_template(
            'thermometers.html',
            thermometers = self.__thermometers.values(),
            **self.__common_args(),
        )

