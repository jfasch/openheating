class HeatingError(Exception):
    def __init__(self, msg, nested_errors=None):
        Exception.__init__(self, msg)
        self.__nested_errors = nested_errors

    def msg(self):
        return self.args[0]
