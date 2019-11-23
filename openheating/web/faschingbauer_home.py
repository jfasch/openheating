from .instance import app


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

@app.flask.route('/')
def home():
    return app.render_template(
        'faschingbauer_home.html',
        thermometers = _thermometer_names,
    )
