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

def configure_from_argparse(args):
    logging.basicConfig(level=args.log_level)

def get_log_config_from_argparse(args):
    return ['--log-level', _level2str(args.log_level)]

async def handle_task_exceptions(awaitable):
    '''To be wrapped around coroutines when they are run by something like
    loop.run_until_complete(coro). Logs exceptions of type Exception
    and terminates the process with failure exitstatus.

    I failed to get loop.set_exception_handler() to work. No
    idea. asyncio is harder than it seems.'''

    try:
        await awaitable
    except Exception:
        logging.exception('Unhandled exception')
        sys.exit(1)
