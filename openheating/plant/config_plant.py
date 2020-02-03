class PlantConfig:
    def __init__(self):
        self.__services = []

    def add_service(self, service):
        if service.busname in [s.busname for s in self.__services]:
            raise DuplicateName(service.busname)
        self.__services.append(service)
    def get_services(self):
        return self.__services

    def parse(self, path):
        context = {
            'ADD_SERVICE': self.add_service,
        }
        with open(path) as f:
            source = f.read()
            code = compile(source, path, 'exec')
            exec(code, context)
