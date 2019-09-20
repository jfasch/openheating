import argparse
import logging


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

def add_log_options(parser):
    levels = ', '.join(('"{}"'.format(levelstr) for levelstr, _ in _levels))
    parser.add_argument('--log-level', 
                        help='Log level (one of {})'.format(levels),
                        type=_str2level,
                        default=logging.NOTSET)

def configure_from_argparse(args):
    logging.basicConfig(level=args.log_level)
