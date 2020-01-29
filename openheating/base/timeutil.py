import datetime
import time


def delta2unix(delta):
    try:
        num = delta.total_seconds()
    except AttributeError: # assume number
        num = delta
    # cap fractional timestamps to entire seconds
    return int(num)

def dt2unix(dt):
    try:
        return dt.timestamp()
    except AttributeError:
        return dt

def unix2dt(ts):
    return datetime.datetime.fromtimestamp(ts)

def now_ts():
    return time.time()
