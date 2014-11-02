import atexit
import os

class PIDFile:
    def __init__(self, filename, main_pid):
        open(filename, 'w').write(str(main_pid))
        atexit.register(_remove_file, main_pid, filename)

def _remove_file(main_pid, filename):
    if os.getpid() == main_pid:
        os.remove(filename)
