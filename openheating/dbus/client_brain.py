from .client import DBusObjectClient

from ..logic.brain import Brain


class DBusBrainClient(DBusObjectClient):
    def think(self):
        dbus_ret = self.client_call('think')

        # cannot use the return value literally. it is littered with
        # DBus data types, like this: 

        # dbus.Array([dbus.Struct((dbus.Int32(0), dbus.Array([dbus.Struct((dbus.String('thinker'), dbus.String('message')), signature=None)], signature=dbus.Signature('(ss)'))), signature=None), dbus.Struct((dbus.Int32(1), dbus.Array([dbus.Struct((dbus.String('thinker'), dbus.String('message')), signature=None)], signature=dbus.Signature('(ss)'))), signature=None)], signature=dbus.Signature('(ia(ss))'))

        ret = []
        for loop_annotation in dbus_ret:
            loopno = int(loop_annotation[0])
            thoughts = []
            for annotation in loop_annotation[1]:
                thoughts.append((str(annotation[0]), str(annotation[1])))
            ret.append((loopno, thoughts))

        return ret
