class ServerObject:
    '''Server side DBus object that wants to know about it being attached
    to and detached from an event loop

    '''

    def startup(self, loop):
        pass
    def shutdown(self):
        pass
