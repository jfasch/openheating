from ..base.error import HeatingError
from ..plant import locations

import os
import unittest
import sys


def run(suite):
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    runner.run(suite)

def find_executable(exe):
    '''Say exe='openheating-blah.py', then this will return
    '/project/root/bin/openheating-blah.py'.

    This mimics the behavior of shutil.which(), hence returns None if
    exe not found.

    '''

    root = locations.find_project_root()
    fullexe = '{}/bin/{}'.format(root, exe)
    if not (os.path.exists(fullexe) or os.path.isfile(fullexe)):
        return None
    return fullexe

