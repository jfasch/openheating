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

    def set_tag(self, tag):
        '''For testing. We only marshal HeatingError instances over DBus,
        losing type information. Code that raises an exception on the
        server side can set a 'tag', so the testing DBus client code
        can check against that.

        '''

        assert 'tag' not in self.__details
        self.__details['tag'] = tag

class ClockSkewError(HeatingError):
    def __init__(self):
        super().__init__('clock skew detected')
