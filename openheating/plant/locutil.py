from ..base.error import HeatingError

import os.path
import sys


def find_project_root():
    '''Based on sys.argv[0], examine the directories upwards towards
    '/'. The first that contains files from the project root
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
        raise HeatingError('cannot find project root (started at {})'.format(start))
