from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..dbus.switch_center import SwitchCenter_Client
from ..dbus.pollable_client import Pollable_Client


class ServiceDefinition:
    def __init__(self, unitname, busname, description, wants, 
                 exe, args=None, pollable_paths=None):
        self.unitname = unitname
        self.busname = busname
        self.description = description
        self.exe = exe
        self.args = []
        if args:
            self.args += args

        self.wants = wants
        self.wantedby = ['multi-user.target'] # hardcoded for now

        self.pollable_paths = []
        if pollable_paths:
            self.pollable_paths += pollable_paths

class MainService(ServiceDefinition):
    def __init__(self, config, wants):
        super().__init__(
            exe='openheating-main.py',
            unitname='openheating-main.service',
            busname=names.Bus.MAIN,
            description='Openheating Main Service',
            wants=wants,
            args=['--config', config])

class ThermometerService(ServiceDefinition):
    def __init__(self, config):
        args = ['--config', config]
        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         unitname='openheating-thermometers.service',
                         description='Openheating Thermometer Service',
                         wants=[],
                         args=args,
                         pollable_paths=['/'])
    def set_simulation_dir(self, d):
        self.args += ['--simulation-dir', d]

class SwitchService(ServiceDefinition):
    def __init__(self, config):
        args = ['--config', config]
        super().__init__(exe='openheating-switches.py',
                         busname=names.Bus.SWITCHES,
                         unitname='openheating-switches.service',
                         description='Openheating Switch Service',
                         wants=[],
                         args=args)
    def set_simulation_dir(self, d):
        self.args += ['--simulation-dir', d]

class CircuitService(ServiceDefinition):
    def __init__(self, config):
        assert type(config) is str
        super().__init__(exe='openheating-circuits.py',
                         busname=names.Bus.CIRCUITS,
                         unitname='openheating-circuits.service',
                         description='Openheating Circuit Service',
                         wants=['openheating-thermometers.service',
                                'openheating-switches.service'],
                         args=['--config', config],
                         pollable_paths=['/'])

class ErrorService(ServiceDefinition):
    def __init__(self):
        super().__init__(
            exe='openheating-errors.py',
            busname=names.Bus.ERRORS,
            unitname='openheating-errors.service',
            description='Openheating Error Service',
            wants=[])

class ExceptionTesterService(ServiceDefinition):
    def __init__(self):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=names.Bus.EXCEPTIONTESTER,
            unitname='openheating-exception-tester.service',
            description='Openheating Exception Tester Service',
            wants=[])

class ManagedObjectTesterService(ServiceDefinition):
    def __init__(self, stampdir):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=names.Bus.MANAGEDOBJECTTESTER,
            unitname='openheating-managedobject-tester.service',
            description='Openheating Managed Object Tester Service',
            wants=[],
            args=['--stamp-directory', stampdir])

class PollWitnessService(ServiceDefinition):
    def __init__(self, witness):
        super().__init__(
            exe='openheating-poll-witness.py',
            busname=names.Bus.POLLWITNESS,
            unitname='openheating-poll-witness.service',
            description='Openheating Poll Witness Service',
            args=['--witness', witness],
            wants=[],
            pollable_paths=['/'])

class CrashTestDummyService(ServiceDefinition):
    def __init__(self, no_busname=False, crash_in_operation_after_nsecs=False):
        args=[]
        if no_busname:
            args.append('--no-busname')
        if crash_in_operation_after_nsecs:
            args += ('--crash-in-operation-after-nsecs', str(crash_in_operation_after_nsecs))

        super().__init__(
            exe='openheating-crash-test-dummy.py',
            busname=names.Bus.CRASHTESTDUMMY,
            unitname='openheating-crash-test-dummy.service',
            description='Openheating Crash Test Dummy Service',
            wants=[],
            args=args)
