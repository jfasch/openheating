class MutantCreator:
    def __init__(self, klass):
        self.__class = klass
    def __call__(self, **kwargs):
        return Mutant(self.__class, **kwargs)

class Mutant:
    def __init__(self, klass, **kwargs):
        self.__class = klass
        self.__kwargs = kwargs
        self.__instance = None

    def __getattr__(self, a):
        if not self.__instance:
            self.__instance = self.__class(**self.__kwargs)
        return _Caller(self.__class, self.__instance, a)

class _Caller:
    def __init__(self, klass, obj, attr):
        self.__class = klass
        self.__obj = obj
        self.__attr = attr
    def __call__(self, *args, **kwargs):
        return self.__class.__dict__[self.__attr](self.__obj, *args, **kwargs)

