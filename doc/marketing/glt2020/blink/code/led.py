class LED_nohw:
    COLORS = {
        'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[1;33m',
    }
    NO_COLOR = '\033[0m'

    def __init__(self, color=None, indent=0):
        self.color = color and self.COLORS[color] or ''
        self.indent = indent
    def on(self):
        print(' '*self.indent, self.color+'on'+self.NO_COLOR)
    def off(self):
        print(' '*self.indent, self.color+'off'+self.NO_COLOR)

