class ClientObject:
    def __init__(self, connection, service, path):
        self.__connection = connection
        service = self.__connection[busname]
        self.__obj = service[path]
        
    def get_interface(self, name):
        return self.__obj.get_interface(name)

class ServerObject:
    '''Server side DBus object that wants to know about it being attached
    to and detached from an event loop

    '''

    def startup(self, loop):
        pass
    def shutdown(self):
        pass
