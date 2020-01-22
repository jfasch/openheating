from . import interface_repo
from . import node
from . import lifecycle
from . import names


@lifecycle.managed(startup='_start', shutdown='_stop')
@node.Definition(interfaces=interface_repo.get(interface_repo.RUNNER))
class Runner_Server:
    def __init__(self, plant, find_exe, bus_kind, common_args):
        self.__plant = plant
        self.__find_exe = find_exe
        self.__bus_kind = bus_kind
        self.__common_args = common_args

    def _start(self):
        self.__plant.startup(
            find_exe=self.__find_exe,
            bus_kind=self.__bus_kind,
            common_args=self.__common_args,
            # don't eat children's stderr but rather let it go
            capture_stderr=False,
        )

    def _stop(self):
        self.__plant.shutdown()
