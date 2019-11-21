from .history_utils import make_histogram_input__full_label
from .instance import app

from ..base import mplutil

import flask
import numpy
from scipy import interpolate

import datetime


@app.flask.route('/')
def home_faschingbauer():
    return app.render_template(
        'home_faschingbauer.html',
        charts = (flask.Markup(_make_svg('Solar', ('SpeicherOben', 'SpeicherMitte', 'SpeicherUnten', 'RuecklaufSolar', 'VorlaufSolar',))),
                  flask.Markup(_make_svg('Oel', ('Oelbrenner',))),
                  flask.Markup(_make_svg('Holz', ('Holzbrenner', 'RuecklaufHolz', 'VorlaufHolz',))),
                  flask.Markup(_make_svg('Kreise', ('VorlaufHeizkreis', 'VorlaufWarmwasser',))),
        ),
    )

def _make_svg(title, thermometernames):
    all_samples = {} # {thermometername: samples}

    # gather raw samples
    granularity = datetime.timedelta(minutes=10)
    duration = datetime.timedelta(days=1)
    for name in thermometernames:
        samples = app.thermometer_histories[name].distill(granularity=granularity,
                                                           duration=duration)
        assert len(samples) > 0
        all_samples[name] = samples

    # find global oldest and youngest samples
    youngest_ts = 0 # epoch; very old
    oldest_ts = datetime.datetime(2500, 1, 1).timestamp() # very young
    maxnum = 0
    for samples in all_samples.values():
        if samples[0][0] < oldest_ts:
            oldest_ts = samples[0][0]
        if samples[-1][0] > youngest_ts:
            youngest_ts = samples[-1][0]
        if len(samples) > maxnum:
            maxnum = len(samples)

    # spline-interpolate and transform onto same time axis.
    uniform_timeaxis = numpy.linspace(oldest_ts, youngest_ts, 
                                      duration.total_seconds()/granularity.total_seconds())
    for samples in all_samples.values():
        if len(samples) <= 3:
            # splrep() requires me to pass more than 3 if I leave k=3
            # (the recommended default). While I don't understand how
            # spline interpolation works, I do accept that it hurts if
            # I don't play by the rules.
            continue
        splinefunc = interpolate.splrep([ts for ts,_ in samples],
                                        [temp for _,temp in samples])
        temperatures = interpolate.splev(uniform_timeaxis, splinefunc)
        samples[:] = list(zip(uniform_timeaxis, temperatures))

    youngest_dt = datetime.datetime.fromtimestamp(youngest_ts)
    oldest_dt = datetime.datetime.fromtimestamp(oldest_ts)

    mplutil.new_plot(title=title, 
                     xlabel='{} - {}'.format(oldest_dt, youngest_dt), 
                     xlim=(oldest_ts, youngest_ts))

    for name, samples in all_samples.items():
        mplutil.plot_samples(samples, label=name)

    return mplutil.plot_as_embeddable_svg()
