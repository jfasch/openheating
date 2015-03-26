class NativeObjectConstructor:
    '''A parameterizable class, used in the service configuration to
    shield the user from all that forking and instantiating that we
    do.

    I suspect I have to look into how descriptors work.
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
    which nothing real is instantiated. Once the service's parent has
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
        return _Caller(self.__instance, a)

class _Caller:
    def __init__(self, obj, attr):
        self.__obj = obj
        self.__attr = attr
    def __call__(self, *args, **kwargs):
        # note that this is not a sign of hardcore python
        # knowledge. need to refine this entire crap
        # thoroughly. investigate on mro, function calls, __getattr__,
        # etc.
        attr = _find_attr_dfs(self.__obj.__class__, self.__attr)
        assert attr, 'attribute '+self.__attr+' not found in '+str(self.__obj)
        return attr(self.__obj, *args, **kwargs)

def _find_attr_dfs(klass, name):
    attr = klass.__dict__.get(name)
    if attr:
        return attr
    for base in klass.__bases__:
        attr = _find_attr_dfs(base, name)
        if attr:
            return attr
    return None
