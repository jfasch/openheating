class HeatingError(Exception):
    def __init__(self, permanent, msg, nested_errors=None):
        assert type(msg) is str
        assert type(permanent) is bool
        assert nested_errors is None or type(nested_errors) is list
        
        Exception.__init__(self, msg)
        self.__permanent = permanent

        if nested_errors is None:
            self.__nested_errors = []
        else:
            self.__nested_errors = nested_errors

    def msg(self):
        return self.args[0]
    def permanent(self):
        return self.__permanent
    def nested_errors(self):
        return self.__nested_errors

    @staticmethod
    def equal(lhs, rhs):
        if isinstance(lhs, HeatingError) ^ isinstance(rhs, HeatingError):
            return False
        if not (isinstance(lhs, HeatingError) and isinstance(rhs, HeatingError)):
            return str(lhs) == str(rhs)
        # both are HeatingError instances
        if lhs.msg() != rhs.msg():
            return False
        if lhs.permanent() != rhs.permanent():
            return False
        if len(lhs.nested_errors()) != len(rhs.nested_errors()):
            return False
        for i in range(len(lhs.nested_errors())):
            if not HeatingError.equal(lhs.nested_errors()[i], rhs.nested_errors()[i]):
                return False
        return True
