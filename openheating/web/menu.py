from collections import namedtuple


Entry = namedtuple('Entry', ('alt', 'url', 'image_url'))
Menu = namedtuple('Menu', ('entries',))
