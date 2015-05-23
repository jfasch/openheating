import logging
import logging.handlers


logger = logging.getLogger()

def init(name, syslog, verbose):
    kwargs = {
        'format': '%(asctime)s %(name)s %(levelname)s:%(message)s',
        'handlers': (syslog and logging.handlers.SysLogHandler(address='/dev/log') or logging.StreamHandler(),),
        
    }
    if verbose:
        kwargs['level'] = logging.DEBUG

    logging.basicConfig(**kwargs)

def enter_child(name):
    global logger
    logger = logging.getLogger(name)


def debug(msg, *args, **kwargs):
    return logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    return logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    return logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    return logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    return logger.critical(msg, *args, **kwargs)

def exception(msg, *args):
    return logger.exception(msg, *args)
    
def log(level, msg, *args, **kwargs):
    return logger.log(level, msg, *args, **kwargs)
