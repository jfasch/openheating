class HeatingException(Exception):
    '''
    Base class for all exceptions thrown here.

    This helps to differentiate between Python SyntaxError,
    ImportError and whatnot, and our own errors.
    '''

    def __init__(self, msg, nested_errors=None):
        Exception.__init__(self, msg)
        self.__nested_errors = nested_errors
        pass
    pass
