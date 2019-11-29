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
