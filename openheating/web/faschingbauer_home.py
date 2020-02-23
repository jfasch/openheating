from .instance import app
from . import svg

import datetime


_top_thermometer_names = (
    'Raum',
    'SpeicherOben',
    'Holzbrenner',
# disable; see thermometers.pyconf:    'Oelbrenner',
)


# move these to some utility module
_one_hour = datetime.timedelta(hours=1)
_one_minute = datetime.timedelta(minutes=1)
_one_day_s = datetime.timedelta(days=1)
_half_an_hour_s = datetime.timedelta(minutes=30)

@app.flask.route('/')
def home():
    return app.render_template(
        'faschingbauer_home.html',
        thermometers = _top_thermometer_names,
        now = datetime.datetime.now(),
        duration = _one_hour,
        granularity = _one_minute,
        svg = svg,
    )
