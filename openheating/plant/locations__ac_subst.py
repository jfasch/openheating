from . import locutil

import os.path


root = locutil.find_project_root()

if root is None:
    bindir = '${bindir}'
    libdir = '${libdir}'
    sharedir = '${sharedir}'
    webdir = '${sharedir}/web'
    confdir = '/etc/openheating'
else:
    bindir = os.path.join(root, 'bin')
    libdir = root
    sharedir = None # don't have such a thing in git
    webdir = os.path.join(root, 'openheating', 'web')

    # faschingbauer will start to suck once there's an alternative :-)
    confdir = os.path.join(root, 'installations', 'faschingbauer')
