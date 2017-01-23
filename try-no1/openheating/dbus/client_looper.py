from .client import DBusObjectClient


class DBusLooperClient(DBusObjectClient):
    def num_loops(self):
        return self.client_call('num_loops')
