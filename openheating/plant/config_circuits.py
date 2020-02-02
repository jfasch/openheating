import logging


class CircuitsConfig:
    def __init__(self):
        self.__circuits = [] # [(name, description, circuit)]

    def get_circuits(self):
        return self.__circuits

    def parse(self, path, bus):
        context = {
            'GET_BUS': lambda: bus,
            'ADD_CIRCUIT': self.__add_circuit,
            'GET_CIRCUITS': self.get_circuits,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)

    def __add_circuit(self, name, description, cls, *args, **kwargs):
        if name in [name for name,_,_ in self.__circuits]:
            raise DuplicateName(name)
        self.__circuits.append((name, description, cls(*args, **kwargs)))
