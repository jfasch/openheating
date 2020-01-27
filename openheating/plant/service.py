from . import dbusutil

from ..base.error import HeatingError
from ..dbus import names
from ..dbus.thermometer_center import ThermometerCenter_Client
from ..dbus.switch_center import SwitchCenter_Client
from ..dbus.pollable_client import Pollable_Client

import pydbus

import tempfile
import subprocess


class BusnameTimeout(HeatingError):
    def __init__(self, msg):
        super().__init__(msg)

class Service:
    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__exe = exe
        if args is None:
            self.__specific_args = []
        else:
            self.__specific_args = args
        self.__bus_kind = None
        self.__process = None # valid once started
        self.__cmdline = None # valid once started
        self.__capture_stderr = None # bool; valid once started

    @property
    def busname(self):
        return self.__busname

    def start(self, find_exe, bus_kind, common_args, capture_stderr):
        assert type(capture_stderr) is bool
        assert self.__bus_kind is None
        assert self.__capture_stderr is None

        self.__bus_kind = bus_kind
        self.__capture_stderr = capture_stderr

        the_exe = find_exe(self.__exe)
        if the_exe is None:
            raise HeatingError('start: {busname}: executable {exe} not found'.format(
                busname=self.__busname, exe=self.__exe))

        argv = [the_exe]
        argv.append(self._oh_bus_arg())
        argv += common_args
        argv += self.__specific_args

        self.__cmdline = ' '.join(argv)

        # start service, and wait until its busname appears.
        self.__insist_busname_available()
        if self.__capture_stderr:
            self.__process = subprocess.Popen(argv, stderr=subprocess.PIPE, universal_newlines=True)
        else:
            self.__process = subprocess.Popen(argv, universal_newlines=True)
        self.__insist_busname_taken()

    def stop(self):
        if self.__process is None:
            raise 

        assert self.__process.returncode is None, "stop() must not be called if start() hasn't succeeded"

        # terminate service process
        self.__process.terminate()
        # our services mess with signals a bit (graceful eventloop
        # termination), so apply a timeout in case anything goes
        # wrong.
        try:
            self.__process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(' '.join(self.__argv), 'refuses to terminate, killing', file=sys.stderr)
            self.__process.kill()
            self.__process.wait()

        # wait for busname to disappear
        with self._bus() as bus:
            proxy = bus.get('org.freedesktop.DBus', '/org/freedesktop/DBus')['org.freedesktop.DBus']
            for _ in range(10):
                if self.__busname in proxy.ListNames():
                    time.sleep(0.5)
                    continue
                else:
                    break
            else:
                # hmm. process has terminated? name still taken?
                self.fail('{busname} still on the bus after "{cmdline}" has exited (?)'.format(
                    busname=self.__busname, cmdline=' '.join(self.__argv)))

        stderr = self.__communicate_get_stderr()

        if self.__process.returncode != 0:
            raise HeatingError('stop: name {busname} exited with status {status}, '
                               'stderr:\n{stderr}'.format(
                                   busname=self.__busname, 
                                   status=self.__process.returncode, 
                                   stderr=_indent_str(stderr)))

        return stderr

    def poll(self, bus, timestamp):
        logging.debug('poll {}, timestamp {}: nothing to do'.format(self.busname, timestamp))

    def _oh_bus_arg(self):
        'openheating service commandline option for bus selection'
        if self.__bus_kind == dbusutil.BUS_KIND_SESSION:
            return '--session'
        if self.__bus_kind == dbusutil.BUS_KIND_SYSTEM:
            return '--system'
        assert False

    def _gdbus_bus_arg(self):
        return self._oh_bus_arg()

    def _bus(self):
        'pydbus.SessionBus() or pydbus.SystemBus()'
        if self.__bus_kind == dbusutil.BUS_KIND_SESSION:
            return pydbus.SessionBus()
        if self.__bus_kind == dbusutil.BUS_KIND_SYSTEM:
            return pydbus.SystemBus()
        assert False

    def __insist_busname_available(self):
        with self._bus() as bus:
            name_occupied = False
            try:
                # this can be done better. for example, don't request
                # the busname (and free it again), but rather ask if
                # it's there.
                with bus.request_name(self.__busname): pass
            except RuntimeError:
                name_occupied = True
            if name_occupied:
                raise HeatingError('start: {busname} already occupied, no point starting "{exe}"'.format(
                    busname=self.__busname, exe=self.__exe))

    def __insist_busname_taken(self):
        for _ in range(5):
            gdbus_wait = ['gdbus', 'wait', self._gdbus_bus_arg(), self.__busname, '--timeout', '1']
            completed_process = subprocess.run(gdbus_wait)
            if completed_process.returncode == 0:
                break

            # busname not yet taken. see if process has exited.
            try:
                self.__process.wait(timeout=0)

                raise HeatingError('start: {busname} not taken within timeout, "{cmdline}" has exited with status {status}, stderr:\n{stderr}'.format(
                    busname=self.__busname,
                    cmdline=self.__cmdline,
                    status=self.__process.returncode,
                    stderr=_indent_str(self.__communicate_get_stderr())))
            except subprocess.TimeoutExpired:
                continue
        else:
            # busname did not appear within the given timeout (5 times
            # 1 second). terminate service process.
            self.__process.terminate()
            self.__process.wait()

            raise BusnameTimeout('start: name {busname} did not appear within timeout: "{cmdline}", stderr:\n{stderr}'.format(
                busname=self.__busname, 
                cmdline=self.__cmdline,
                stderr=_indent_str(self.__communicate_get_stderr())))

    def __communicate_get_stderr(self):
        _, stderr = self.__process.communicate()
        if self.__capture_stderr:
            return stderr
        assert stderr is None
        return '(stderr not captured)'


def _indent_str(s):
    return '\n'.join(['  * '+line for line in s.split('\n')])

class MainService(Service):
    def __init__(self, config):
        super().__init__(
            exe='openheating-main.py',
            busname=names.Bus.MAIN,
            args=['--config', config])

class ThermometerService(Service):
    def __init__(self, config, background_updates=True, simulation_dir=None):
        self.__simulation_dir = simulation_dir

        args = ['--config', config]
        if self.__simulation_dir is not None:
            args += ['--simulation-dir', self.__simulation_dir]
        if not background_updates:
            args += ['--update-interval', '0']

        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         args=args)

    @property
    def simulation_dir(self):
        return self.__simulation_dir

    def center_client(self, bus):
        '''convenience method, for use by tests'''
        return ThermometerCenter_Client(bus)
    def thermometer_client(self, bus, name):
        '''convenience method, for use by tests'''
        return ThermometerCenter_Client(bus).get_thermometer(name)        

class SwitchService(Service):
    def __init__(self, config, simulation_dir=None):
        self.__simulation_dir = simulation_dir

        args = ['--config', config]
        if self.__simulation_dir is not None:
            args += ['--simulation-dir', self.__simulation_dir]

        super().__init__(exe='openheating-switches.py',
                         busname=names.Bus.SWITCHES,
                         args=args)

    @property
    def simulation_dir(self):
        return self.__simulation_dir

    def switch_client(self, bus, name):
        '''convenience method, for use by tests'''
        return SwitchCenter_Client(bus).get_switch(name)

class CircuitService(Service):
    def __init__(self, config):
        assert type(config) is str
        super().__init__(exe='openheating-circuits.py',
                         busname=names.Bus.CIRCUITS,
                         args=['--config', config])

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
