from . import config
from .service import MainService

from openheating.base.error import HeatingError

import sys


def create_plant_with_main(plant_config_file):
    plant_config = config.PlantConfig()
    plant_config.parse(plant_config_file)
    
    services = plant_config.get_services()
    services.append(MainService(config=plant_config_file))
    return Plant(services)

class Plant:
    def __init__(self, services):
        self.__registered_services = services[:]
        self.__running_services = []
        self.__running = False
        self.__capture_stderr = None # bool; valid after startup

    @property
    def running(self):
        return self.__running

    @property
    def running_services(self):
        return self.__running_services

    def startup(self, find_exe, bus_kind, common_args, capture_stderr):
        assert type(capture_stderr) is bool
        self.__capture_stderr = capture_stderr

        started = []
        start_error = None
        while len(self.__registered_services):
            s = self.__registered_services[0]
            s.start(find_exe=find_exe, bus_kind=bus_kind, common_args=common_args, capture_stderr=self.__capture_stderr)
            del self.__registered_services[0]
            self.__running_services.insert(0, s)
        self.__running = True

    def shutdown(self, print_stderr=False):
        assert not print_stderr or self.__capture_stderr, 'can only print stderr when captured'

        stderrs = []
        errors = []

        for s in reversed(self.__running_services):
            try:
                stderr = s.stop()
                stderrs.append((s.busname, stderr))
            except Exception as e:
                errors.append(e)

        if print_stderr or len(errors):
            for busname, stderr in stderrs:
                print('\n*** STDERR from {}'.format(busname), file=sys.stderr)
                if stderr is None:
                    print(' '*3, '(apparently unstarted)', file=sys.stderr)
                else:
                    for line in stderr.split('\n'):
                        print(' '*3, line, file=sys.stderr)

        if len(errors):
            msg = ['there were errors while stopping services ...']
            for e in errors:
                msg.append(str(e))
            raise RuntimeError('\n'.join(msg))

        self.__running = False
