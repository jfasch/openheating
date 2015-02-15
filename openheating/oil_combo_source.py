from .source import Source


class OilComboSource(Source):
    def __init__(self, name, oil_combo):
        Source.__init__(self, name)

        self.__oil_combo = oil_combo

    def temperature(self):
        return self.__oil_combo.temperature()

    def do_request(self):
        self.__oil_combo.request()

    def do_release(self):
        self.__oil_combo.release()
