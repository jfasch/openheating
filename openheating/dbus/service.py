from .rebind import DBusServerConnection
from .thermometer_object import DBusThermometerObject
from .switch_object import DBusSwitchObject
from .thermometer_center_object import DBusThermometerCenterObject
from .switch_center_object import DBusSwitchCenterObject

from ..switch_center import SwitchCenter
from ..thermometer_center import ThermometerCenter
from ..switch import Switch
from ..thermometer import Thermometer

class DBusService:
    def __init__(self, creators):
        self.__creators = creators
        self.__dbus_objects = {}

    def create_dbus_objects(self, connection):
        # DBus objects are supposed to be created only once
        assert len(self.__dbus_objects) == 0

        # wrap DBus objects around the native ones
        for path, creator in self.__creators.items():
            local_object = creator.create(connection=connection)

            if isinstance(local_object, SwitchCenter):
                dbus_object = DBusSwitchCenterObject(
                    connection=connection,
                    object_path=path, center=local_object)
            elif isinstance(local_object, ThermometerCenter):
                dbus_object = DBusThermometerCenterObject(
                    connection=connection,
                    object_path=path, center=local_object)
            elif isinstance(local_object, Thermometer):
                dbus_object = DBusThermometerObject(
                    connection=connection,
                    object_path=path, thermometer=local_object)
            elif isinstance(local_object, Switch):
                dbus_object = DBusSwitchObject(
                    connection=connection,
                    object_path=path, switch=local_object)
            else:
                assert False, local_object

            self.__dbus_objects[path] = dbus_object

    def num_dbus_objects__test(self):
        return len(self.__dbus_objects)

    def get_dbus_object__test(self, path):
        return self.__dbus_objects.get(path)
