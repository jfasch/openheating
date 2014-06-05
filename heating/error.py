class HeatingException(Exception):
    '''
    Base class for all exception thrown here.

    This helps to differentiate between Python SyntaxError,
    ImportError and whatnot, and our own errors.
    '''

    def __init__(self, msg):
        Exception.__init__(self, msg)
        pass
    pass
