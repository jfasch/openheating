import argparse
import logging
import sys
import traceback
import textwrap


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
    class IndentExceptionFormatter(logging.Formatter):
        def __init__(self, *args, exc_prefix, **kwargs):
            super().__init__(*args, **kwargs)
            self.__exc_prefix = exc_prefix
        def formatException(self, exc_info):
            block = ''.join(traceback.format_exception(*exc_info))
            block = textwrap.indent(text=block, prefix=self.__exc_prefix)
            return block
    
    formatter = IndentExceptionFormatter(
        '%(asctime)s:%(levelname)s:{componentname}:%(name)s: %(message)s'.format(componentname=componentname),
        exc_prefix='    *** ')
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(args.log_level)
    logging.getLogger().addHandler(stderr_handler)

def get_log_config_from_argparse(args):
    return ['--log-level', _level2str(args.log_level)]
