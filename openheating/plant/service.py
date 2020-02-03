from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..dbus.switch_center import SwitchCenter_Client
from ..dbus.pollable_client import Pollable_Client

import logging


class Service:
    def __init__(self, busname, exe, args=None):
        self.busname = busname
        self.exe = exe
        self.args = []
        if args:
            self.args += args

    def poll(self, bus, timestamp):
        logging.debug('poll {}, timestamp {}: nothing to do'.format(self.busname, timestamp))

class MainService(Service):
    def __init__(self, config):
        super().__init__(
            exe='openheating-main.py',
            busname=names.Bus.MAIN,
            args=['--config', config])

class ThermometerService(Service):
    def __init__(self, config):
        args = ['--config', config]
        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         args=args)
    def set_simulation_dir(self, d):
        self.args += ['--simulation-dir', d]
    def center_client(self, bus):
        '''convenience method, for use by tests'''
        return ThermometerCenter_Client(bus)
    def thermometer_client(self, bus, name):
        '''convenience method, for use by tests'''
        return ThermometerCenter_Client(bus).get_thermometer(name)
    def poll(self, bus, timestamp):
        pollable_client = Pollable_Client(bus=bus, busname=names.Bus.THERMOMETERS, path='/')
        return pollable_client.poll(timestamp)

class SwitchService(Service):
    def __init__(self, config):
        args = ['--config', config]
        super().__init__(exe='openheating-switches.py',
                         busname=names.Bus.SWITCHES,
                         args=args)
    def set_simulation_dir(self, d):
        self.args += ['--simulation-dir', d]
    def switch_client(self, bus, name):
        '''convenience method, for use by tests'''
        return SwitchCenter_Client(bus).get_switch(name)

class CircuitService(Service):
    def __init__(self, config):
        assert type(config) is str
        super().__init__(exe='openheating-circuits.py',
                         busname=names.Bus.CIRCUITS,
                         args=['--config', config])

    def poll(self, bus, timestamp):
        pollable_client = Pollable_Client(bus=bus, busname=names.Bus.CIRCUITS, path='/')
        return pollable_client.poll(timestamp)

class ErrorService(Service):
    def __init__(self):
        super().__init__(
            exe='openheating-errors.py',
            busname=names.Bus.ERRORS)

class ExceptionTesterService(Service):
    def __init__(self):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=names.Bus.EXCEPTIONTESTER,
        )

class ManagedObjectTesterService(Service):
    def __init__(self, stampdir):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=names.Bus.MANAGEDOBJECTTESTER,
            args=['--stamp-directory', stampdir],
        )

class PollWitnessService(Service):
    def __init__(self, witness):
        super().__init__(
            exe='openheating-poll-witness.py',
            busname=names.Bus.POLLWITNESS,
            args=['--witness', witness])

    def poll(self, bus, timestamp):
        client = Pollable_Client(bus=bus, busname=names.Bus.POLLWITNESS, path='/')
        client.poll(timestamp)

class CrashTestDummyService(Service):
    def __init__(self, no_busname=False, crash_in_operation_after_nsecs=False):
        args=[]
        if no_busname:
            args.append('--no-busname')
        if crash_in_operation_after_nsecs:
            args += ('--crash-in-operation-after-nsecs', str(crash_in_operation_after_nsecs))

        super().__init__(
            exe='openheating-crash-test-dummy.py',
            busname=names.Bus.CRASHTESTDUMMY,
            args=args)
