from .config_plant import PlantConfig
from .service import MainService
from .service import ThermometerService
from .service import SwitchService
from .service_runner import ServiceRunner

from openheating.base.error import HeatingError

import sys
import os


def create_plant_with_main(plant_config_file):
    plant_config = PlantConfig()
    plant_config.parse(plant_config_file)
    
    services = plant_config.get_services()
    services.append(MainService(config=plant_config_file))
    return Plant(services)

class Plant:
    def __init__(self, services):
        self.__running = False
        self.__capture_stderr = None # bool; valid after startup

        self.__simulation_dir = None
        self.__thermometers_dir = None
        self.__switches_dir = None

        self.__services = services[:]
        self.__service_runners = []

        # thermometers and switches are special, especially for tests
        # and/or simulation. sniff on those, out of pure convenience.
        self.__thermometer_service = None
        self.__switch_service = None

        for s in self.__services:
            if isinstance(s, ThermometerService):
                self.__thermometer_service = s
            if isinstance(s, SwitchService):
                self.__switch_service = s

    @property
    def running(self):
        return self.__running

    @property
    def thermometer_service(self):
        return self.__thermometer_service
    @property
    def switch_service(self):
        return self.__switch_service

    @property
    def services(self):
        return self.__services

    def enable_simulation_mode(self, simulation_dir):
        self.__simulation_dir = simulation_dir
        self.__thermometers_dir = simulation_dir + '/thermometers'
        self.__switches_dir = simulation_dir + '/switches'

        os.makedirs(self.__thermometers_dir, exist_ok=True)
        os.makedirs(self.__switches_dir, exist_ok=True)

        if self.__thermometer_service:
            self.__thermometer_service.set_simulation_dir(self.__thermometers_dir)
        if self.__switch_service:
            self.__switch_service.set_simulation_dir(self.__switches_dir)
        
        return self.__thermometers_dir, self.__switches_dir

    def startup(self, find_exe, bus_kind, common_args, capture_stderr):
        assert type(capture_stderr) is bool
        self.__capture_stderr = capture_stderr

        started = []
        start_error = None
        for service in self.__services:
            runner = ServiceRunner(service)
            runner.start(find_exe=find_exe, bus_kind=bus_kind, common_args=common_args, capture_stderr=self.__capture_stderr)
            self.__service_runners.append(runner)
        self.__running = True

    def shutdown(self, print_stderr=False):
        assert not print_stderr or self.__capture_stderr, 'can only print stderr when captured'

        stderrs = []
        errors = []

        for runner in reversed(self.__service_runners):
            try:
                stderr = runner.stop()
                stderrs.append((runner.servicedef.busname, stderr))
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
