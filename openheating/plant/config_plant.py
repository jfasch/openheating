class PlantConfig:
    def __init__(self):
        self.__servicedefs = []

    def add_servicedef(self, servicedef):
        if servicedef.busname in [s.busname for s in self.__servicedefs]:
            raise DuplicateName(servicedef.busname)
        self.__servicedefs.append(servicedef)
    def get_servicedefs(self):
        return self.__servicedefs

    def parse(self, path):
        context = {
            'ADD_SERVICE': self.add_servicedef,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)
