from .history_utils import make_histogram_input__full_label

from .instance import app

import datetime


@app.flask.route('/')
def home_faschingbauer():
    solar = Group('solar', ('SpeicherOben', 'SpeicherMitte', 'SpeicherUnten', 'RuecklaufSolar', 'VorlaufSolar',))
    oel = Group('oel', ('Oelbrenner',))
    holz = Group('holz', ('Holzbrenner', 'RuecklaufHolz', 'VorlaufHolz',))
    kreise = Group('kreise', ('VorlaufHeizkreis', 'VorlaufWarmwasser',))

    return app.render_template(
        'home_faschingbauer.html',
        solar=solar,
        oel=oel,
        holz=holz,
        kreise=kreise)

class Group:
    def __init__(self, name, thermometernames):
        self.__name = name
        self.__histories = {}
        for tname in thermometernames:
            self.__histories[tname] = make_histogram_input__full_label(app.thermometer_histories[tname].distill(
                granularity=datetime.timedelta(minutes=1),
                duration=datetime.timedelta(days=1)))

    @property
    def name(self):
        return self.__name

    def items(self):
        yield from self.__histories.items()

    def __getitem__(self, thermometername):
        return self.__histories[thermometername]
