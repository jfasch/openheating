class NativeObjectConstructor:
    '''A parameterizable class, used in the service configuration to
    shield the user from all that forking and instantiating that we
    do.
    '''

    def __init__(self, klass):
        self.__class = klass
    def __call__(self, **kwargs):
        return NativeObject(self.__class, **kwargs)

class NativeObject:
    '''Defers instantiation of _real_ objects until they are first
    used. Parameterized with the real object's class and ctor
    parameters.

    NativeObject instances are created in a service's parent process
    where nothing real is instantiated. Once the service's parent has
    forked the final service process, NativeObject instances are used
    as if they were real objects, and that's the time where
    instantiation takes place.
    '''

    def __init__(self, klass, **kwargs):
        self.__class = klass
        self.__kwargs = kwargs
        self.__instance = None

    def __getattr__(self, a):
        if not self.__instance:
            self.__instance = self.__class(**self.__kwargs)
        return getattr(self.__instance, a)
