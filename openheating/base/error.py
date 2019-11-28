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
