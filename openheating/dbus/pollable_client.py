from . import interface_repo
from . import error
from . import _util


class Pollable_Client:
    def __init__(self, bus, busname, path):
        self.__iface = _util.get_iface(
            bus=bus,
            busname=busname,
            path=path,
            iface=interface_repo.POLLABLE)

    @error.maperror
    def poll(self, timestamp):
        return self.__iface.poll(timestamp)
