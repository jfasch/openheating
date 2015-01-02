from ..config_parser import ConfigParser

from ..error import HeatingError

class DBusServiceConfig:
    DAEMON_ADDRESS = 'DAEMON_ADDRESS'
    BUS_NAME = 'BUS_NAME'
    
    def __init__(self, symbols, content):
        parser = ConfigParser(symbols=symbols)
        self.__config = parser.parse(content)
        
        self.__daemon_address = self.__config.get('DAEMON_ADDRESS')
        self.__bus_name = self.__config.get('BUS_NAME')

        # early sanity
        if self.__daemon_address is None:
            raise HeatingError('"DAEMON_ADDRESS" not specified')
        assert type(self.__daemon_address) is str

        if self.__bus_name is None:
            raise HeatingError('"BUS_NAME" not specified')
        assert type(self.__bus_name) is str
    
    def daemon_address(self):
        return self.__daemon_address
    def bus_name(self):
        return self.__bus_name

    # for derived classes
    def config(self):
        return self.__config
