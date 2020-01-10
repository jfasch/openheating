from ..base.error import HeatingError

import os
import unittest


def run(suite):
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    runner.run(suite)

def find_project_root():
    '''Given that os.getcwd() reports a directory inside the source tree,
    find the root of the source tree.'''

    start = root = os.getcwd()
    while root != '/':
        if os.path.isfile(root + '/setup.py') and \
           os.path.isfile(root + '/README.rst'):
            return root
        root = os.path.normpath(os.path.join(root, '..'))
    else:
        raise HeatingError('cannot find project root (started at {})'.format(start))
    
def find_executable(exe):
    '''Say exe='openheating-blah.py', then this will return
    '/project/root/bin/openheating-blah.py'.

    This mimics the behavior of shutil.which(), hence returns None if
    exe not found.

    '''

    root = find_project_root()
    fullexe = '{}/bin/{}'.format(root, exe)
    if not (os.path.exists(fullexe) or os.path.isfile(fullexe)):
        return None
    return fullexe

