from .instance import app

import datetime


_thermometer_names = (
    'Raum',
    'SpeicherOben',
    'Holzbrenner',
    'Oelbrenner',

    'VorlaufHeizkreis',
    'VorlaufWarmwasser',
    'VorlaufSolar',
    'VorlaufHolz',

    'SpeicherMitte',
    'SpeicherUnten',
    'RuecklaufSolar',

    'RuecklaufHolz',
)


_one_day_s = int(datetime.timedelta(days=1).total_seconds())
_half_an_hour_s = int(datetime.timedelta(minutes=30).total_seconds())

@app.flask.route('/')
def home():
    return app.render_template(
        'faschingbauer_home.html',
        thermometers = _thermometer_names,
        duration = _one_day_s,
        granularity = _half_an_hour_s,
    )
