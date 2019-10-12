from ..error import HeatingError

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
           os.path.isfile(root + '/README.md'):
            return root
        root = os.path.normpath(os.path.join(root, '..'))
    else:
        raise HeatingError('cannot find project root (started at {})'.format(start))
    
def find_executable(exe):
    '''Say exe=='openheating-blah.py', then this will return
    '/project/root/bin/openheating-blah.py'.'''

    root = find_project_root()
    fullexe = '{}/bin/{}'.format(root, exe)
    if not os.path.exists(fullexe):
        raise HeatingError('{} does not exist'.format(fullexe))
    if not os.path.isfile(fullexe):
        raise HeatingError('{} is not a file'.format(fullexe))
    return fullexe
