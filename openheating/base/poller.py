import logging


class Poller:
    def __init__(self, timestamps, pollables=None):
        self.__pollables = pollables
        self.__timiter = iter(timestamps)

    def poll_n(self, n, msg=None):
        dmsg = 'poll {} times'.format(n)
        if msg:
            dmsg += ': ' + msg
        logging.debug(dmsg)
        while n > 0:
            ts = next(self.__timiter)
            self.__poll(ts)
            n -= 1

    def __poll(self, timestamp):
        for p in self.__pollables:
            p.poll(timestamp)

