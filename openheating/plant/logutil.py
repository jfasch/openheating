import argparse
import logging
import sys


_levels = (
    ('critical', logging.CRITICAL),
    ('error', logging.ERROR),
    ('warning', logging.WARNING),
    ('info', logging.INFO),
    ('debug', logging.DEBUG)
)

def _str2level(s):
    for levelstr, level in _levels:
        if s == levelstr:
            return level
    else:
        raise argparse.ArgumentTypeError('invalid log level: '+s)

def _level2str(l):
    for levelstr, level in _levels:
        if l == level:
            return levelstr
    else:
        assert False, 'level {} not found'.format(l)

def add_log_options(parser):
    levels = ', '.join(('"{}"'.format(levelstr) for levelstr, _ in _levels))
    parser.add_argument('--log-level', 
                        help='Log level (one of {})'.format(levels),
                        type=_str2level,
                        default=logging.WARNING)

def configure_from_argparse(args, componentname):
    logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s:%(levelname)s:{componentname}:%(name)s: %(message)s'.format(componentname=componentname))

def get_log_config_from_argparse(args):
    return ['--log-level', _level2str(args.log_level)]
