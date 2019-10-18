from gi.repository import GLib

import logging
import signal
import os


lifecycle_logger = logging.getLogger('lifecycle')

class GracefulTermination:
    '''Implements the 'self pipe trick',
    http://man7.org/tlpi/code/online/diff/altio/self_pipe.c.html, to
    gracefully terminate the loop.

    '''

    def __init__(self, loop, signals):
        self.__loop = loop
        self.__requested = False
        self.__signals = list(signals)

        # I'd rather use eventfd(2), but a pipe is more readily
        # available in python.
        self.__pipe = os.pipe()
        # doing the self pipe trick, we watch pipe[0] (the
        # read-side). glib hands us a 'tag' which is used to remove
        # the watch later.
        self.__rfd_tag = None

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, *args):
        self.uninstall()
        return False # dont suppress exceptions

    @property
    def requested(self):
        return self.__requested

    def install(self):
        for sig in self.__signals:
            signal.signal(sig, self.__sighandler)
            r,_ = self.__pipe
        self.__rfd_tag = GLib.io_add_watch(r, GLib.IO_IN, self.__terminate_iocallback)

    def uninstall(self):
        r,_ = self.__pipe
        ok = GLib.source_remove(self.__rfd_tag)
        assert ok

        for sig in self.__signals:
            signal.signal(sig, signal.SIG_DFL)

    def __sighandler(self, signal, frame):
        lifecycle_logger.info('signal {} received, sending termination request'.format(signal))
        self.__requested = True
        _,w = self.__pipe
        os.write(w,b'q')

    def __terminate_iocallback(self, source, condition):
        lifecycle_logger.info('termination request seen, terminating')
        r,_ = self.__pipe
        # paranoia
        assert source == r
        assert condition == GLib.IO_IN

        # read from pipe so event does not keep firing
        os.read(r, 1)

        self.__loop.quit()
        return True # keep watching
