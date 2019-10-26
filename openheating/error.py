class HeatingError(Exception):
    def __init__(self, msg=None, details=None):
        if details is None:
            assert msg is not None
            self.__details = {
                'category': 'general',
                'message': msg,
            }
        else:
            self.__details = details

        super().__init__(self.__details['message'])

    @property
    def details(self):
        return self.__details

class BadDBusPathComponent(HeatingError):
    """Used where e.g. a thermometer configuration gives the thermometer
    a name that is unusable in a DBus object path"""
    def __init__(self, name):
        super().__init__(msg='{} is not a valid DBus object path component'.format(name))
