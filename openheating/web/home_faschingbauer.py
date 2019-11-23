from .history_utils import make_histogram_input__full_label
from .instance import app

import flask
import numpy
from scipy import interpolate

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

@app.flask.route('/')
def home_faschingbauer():
    return app.render_template(
        'home_faschingbauer.html',
        thermometers = _thermometer_names,
    )
