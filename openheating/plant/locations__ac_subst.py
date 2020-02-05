from . import locutil

import os.path


root = locutil.find_project_root()

if root is None:
    bindir = '${bindir}'
    libdir = '${libdir}'
    confdir = '/etc/openheating'
else:
    bindir = os.path.join(root, 'bin')
    libdir = root
    # faschingbauer will start to suck once there's an alternative :-)
    confdir = os.path.join(root, 'installations', 'faschingbauer')
