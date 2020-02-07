from ..base.error import HeatingError

import os.path
import sys


def find_project_root():
    '''Based on sys.argv[0], examine the directories upwards towards
    '/'. The first directory that contains files from the project root
    (README.rst is a candidate) is considered the project root
    directory.

    If no such directory is encountered None is returned, indicating
    that the command has been run from $PATH.

    '''

    start = root = os.path.dirname(sys.argv[0])
    while root != '/':
        if os.path.isfile(root + '/setup.py') and \
           os.path.isfile(root + '/README.rst'):
            return root
        root = os.path.normpath(os.path.join(root, '..'))
    else:
        return None


root = find_project_root()

if root is None:
    # running from an installed location. setup.py has generated the
    # location information into 'installed.py' which is only available
    # in that - installed - case.
    from . import installed

    bindir = installed.bindir
    libdir = installed.libdir
    sharedir = installed.sharedir
    webdir = installed.webdir
    confdir = installed.confdir
else:
    bindir = os.path.join(root, 'bin')
    libdir = root
    sharedir = None # don't have such a thing in git
    webdir = os.path.join(root, 'openheating', 'web')

    # faschingbauer will start to suck once there's an alternative :-)
    confdir = os.path.join(root, 'installations', 'faschingbauer')


def find_executable(exe):
    '''Depending on sys.argv[0], return the absolute path to the
    executable.
    '''

    fullexe = os.path.join(bindir, exe)
    if not (os.path.exists(fullexe) or os.path.isfile(fullexe)):
        raise HeatingError('executable {} not found in {}'.format(exe, bindir))
    return fullexe
