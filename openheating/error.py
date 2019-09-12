class HeatingError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class BadDBusPathComponent(HeatingError):
    """Used where e.g. a thermometer configuration gives the thermometer
    a name that is unusable in a DBus object path"""
    def __init__(self, name):
        super().__init__(msg='{} is not a valid DBus object path component'.format(name))
