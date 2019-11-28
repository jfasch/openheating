from openheating.base.error import HeatingError


class DuplicateError(HeatingError):
    def __init__(self, name):
        super().__init__(msg='duplicate detected: "{}"'.format(name))
        self.name = name
    

def read_switches(thing):
    context = {}
    exec(_make_code(thing), context)
    
    switches = context.get('SWITCHES')
    if switches is None:
        raise HeatingError('SWITCHES (iterable) expected but not there')

    names = set()
    for s in switches:
        if s.get_name() in names:
            raise DuplicateError(s.get_name())
        names.add(s.get_name())

    return switches

def _make_code(thing):
    if hasattr(thing, 'read'):
        code = thing.read()
    elif type(thing) is str:
        code = thing
    else:
        code = '\n'.join(thing)
    return code

