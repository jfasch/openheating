from openheating.base.error import HeatingError
from openheating.dbus import names

import pydbus

import tempfile
import subprocess


class Service:
    BUS_KIND_SESSION = 7
    BUS_KIND_SYSTEM = 42

    def __init__(self, busname, exe, args=None):
        self.__busname = busname
        self.__exe = exe
        self.__args = args
        self.__process = None
        self.__bus_kind = None

    @property
    def busname(self):
        return self.__busname

    def start(self, find_exe, bus_kind, debug):
        assert self.__bus_kind is None
        self.__bus_kind = bus_kind

        the_exe = find_exe(self.__exe)
        if the_exe is None:
            raise HeatingError('start: {busname}: executable {exe} not found'.format(
                busname=self.__busname, exe=self.__exe))

        argv = [the_exe]
        argv.append(self._oh_bus_arg())
        if debug:
            argv += ['--log-level', 'debug']
        if self.__args is not None:
            argv += self.__args

        service_cmdline = ' '.join(argv)

        # start service, and wait until its busname appears.
        self.__insist_busname_available()
        self.__process = subprocess.Popen(argv, stderr=subprocess.PIPE, universal_newlines=True)
        self.__insist_busname_taken()

    def stop(self):
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

        _, stderr = self.__process.communicate()

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

        if self.__process.returncode != 0:
            raise HeatingError('stop: name {busname} exited with status {status}, '
                               'stderr:\n{stderr}'.format(
                                   busname=self.__busname, 
                                   status=self.__process.returncode, 
                                   stderr=_indent_str(stderr)))

        return stderr

    def _oh_bus_arg(self):
        'openheating service commandline option for bus selection'
        if self.__bus_kind == Service.BUS_KIND_SESSION:
            return '--session'
        if self.__bus_kind == Service.BUS_KIND_SYSTEM:
            return '--system'
        assert False

    def _gdbus_bus_arg(self):
        return self._oh_bus_arg()

    def _bus(self):
        'pydbus.SessionBus() or pydbus.SystemBus()'
        if self.__bus_kind == Service.BUS_KIND_SESSION:
            return pydbus.SessionBus()
        if self.__bus_kind == Service.BUS_KIND_SYSTEM:
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
                _, stderr = self.__process.communicate()

                raise HeatingError('start: {busname} not taken within timeout, "{cmdline}" has exited with status {status}, stderr:\n{stderr}'.format(
                    busname=self.__busname,
                    cmdline=service_cmdline,
                    status=self.__process.returncode,
                    stderr=_indent_str(stderr)))
            except subprocess.TimeoutExpired:
                continue
        else:
            # busname did not appear within the given timeout (5 times
            # 1 second). terminate service process.
            self.__process.terminate()
            self.__process.wait()
            _, stderr = self.__process.communicate()
            raise HeatingError('start: name {busname} did not appear within timeout: "{cmdline}", stderr:\n{stderr}'.format(
                busname=self.__busname, 
                cmdline=service_cmdline,
                stderr=_indent_str(stderr)))

def _indent_str(s):
    return s.replace('\n', '\n    ')

class ThermometerService(Service):
    def __init__(self, config, simulated_thermometers_dir=None, debug=False):
        assert type(config) is str
        args = ['--config', config]
        if simulated_thermometers_dir is not None:
            args += ['--simulated-thermometers-dir', simulated_thermometers_dir]

        super().__init__(exe='openheating-thermometers.py',
                         busname=names.Bus.THERMOMETERS,
                         args=args)

class SwitchService(Service):
    def __init__(self, config, simulated_switches_dir=None, debug=False):
        assert type(config) is str
        args = ['--config', config]
        if simulated_switches_dir is not None:
            args += ['--simulated-switches-dir', simulated_switches_dir]

        super().__init__(exe='openheating-switches.py',
                         busname=names.Bus.SWITCHES,
                         args=args)

class CircuitService(Service):
    def __init__(self, config, debug=False):
        assert type(config) is str
        super().__init__(exe='openheating-circuits.py',
                         busname=names.Bus.CIRCUITS,
                         args=['--config', config])

class ErrorService(Service):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-errors.py',
            busname=names.Bus.ERRORS)

class ExceptionTesterService(Service):
    def __init__(self, debug=False):
        super().__init__(
            exe='openheating-exception-tester.py',
            busname=names.Bus.EXCEPTIONTESTER,
        )

class ManagedObjectTesterService(Service):
    def __init__(self, stampdir, debug=False):
        super().__init__(
            exe='openheating-managedobject-tester.py',
            busname=names.Bus.MANAGEDOBJECTTESTER,
            args=['--stamp-directory', stampdir],
        )
