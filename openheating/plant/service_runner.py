from ..base.error import HeatingError

from . import dbusutil

import pydbus

import logging
import subprocess


class BusnameTimeout(HeatingError):
    def __init__(self, msg):
        super().__init__(msg)

class ServiceRunner:
    def __init__(self, servicedef):
        self.__servicedef = servicedef

        self.__bus_kind = None
        self.__process = None # valid once started
        self.__cmdline = None # valid once started
        self.__capture_stderr = None # bool; valid once started

    @property
    def servicedef(self):
        return self.__servicedef

    def start(self, find_exe, bus_kind, common_args, capture_stderr):
        assert type(capture_stderr) is bool
        assert self.__bus_kind is None
        assert self.__capture_stderr is None

        self.__bus_kind = bus_kind
        self.__capture_stderr = capture_stderr

        the_exe = find_exe(self.__servicedef.exe)
        if the_exe is None:
            raise HeatingError('start: {busname}: executable {exe} not found'.format(
                busname=self.__servicedef.busname, exe=self.servicedef.exe))

        argv = [the_exe]
        argv.append(self._oh_bus_arg())
        argv += common_args
        argv += self.__servicedef.args

        self.__cmdline = ' '.join(argv)

        # start service, and wait until its busname appears.
        logging.debug('starting {} ({})'.format(self.__servicedef.busname, ' '.join(argv)))
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
                if self.__servicedef.busname in proxy.ListNames():
                    time.sleep(0.5)
                    continue
                else:
                    break
            else:
                # hmm. process has terminated? name still taken?
                self.fail('{busname} still on the bus after "{cmdline}" has exited (?)'.format(
                    busname=self.__servicedef.busname, cmdline=' '.join(self.__argv)))

        stderr = self.__communicate_get_stderr()

        if self.__process.returncode != 0:
            raise HeatingError('stop: name {busname} exited with status {status}, '
                               'stderr:\n{stderr}'.format(
                                   busname=self.__servicedef.busname, 
                                   status=self.__process.returncode, 
                                   stderr=_indent_str(stderr)))

        return stderr

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
                with bus.request_name(self.__servicedef.busname): pass
            except RuntimeError:
                name_occupied = True
            if name_occupied:
                raise HeatingError('start: {busname} already occupied, no point starting "{exe}"'.format(
                    busname=self.__servicedef.busname, exe=self.__servicedef.exe))

    def __insist_busname_taken(self):
        for _ in range(5):
            gdbus_wait = ['gdbus', 'wait', self._gdbus_bus_arg(), self.__servicedef.busname, '--timeout', '1']
            completed_process = subprocess.run(gdbus_wait)
            if completed_process.returncode == 0:
                break

            # busname not yet taken. see if process has exited.
            try:
                self.__process.wait(timeout=0)

                raise HeatingError('start: {busname} not taken within timeout, "{cmdline}" has exited with status {status}, stderr:\n{stderr}'.format(
                    busname=self.__servicedef.busname,
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
                busname=self.__servicedef.busname, 
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
