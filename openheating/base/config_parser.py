class ConfigParser:
    def __init__(self, symbols):
        self.__symbols = symbols

    def parse(self, content, filename):
        # compile content for later exec(). exec() could take a string
        # and compile that by itself, but it does not take a hint as
        # to which file the string was read from. compile() does, and
        # it prints the filename hint in an error - this helps the
        # poor user.
        code = compile(content, filename, 'exec')

        context = {}
        context.update(self.__symbols)
        exec(code, context)
        return context
