from .instance import app
from ..base import mplutil

import flask
import numpy
from scipy import interpolate

import datetime


def url_for_chart(names, xsize=None, ysize=None, duration=None, granularity=None):
    params = ['names=' + str(names)]
    if xsize is not None:
        params.append('xsize={}'.format(xsize))
    if ysize is not None:
        params.append('ysize={}'.format(ysize))
    if duration is not None:
        try:
            duration = duration.total_seconds()
        except AttributeError:
            pass
        params.append('duration={}'.format(duration))
    if granularity is not None:
        try:
            granularity = granularity.total_seconds()
        except AttributeError:
            pass
        params.append('granularity={}'.format(granularity))

    url = flask.url_for('temperature_chart')
    if len(params):
        url += '?'
        url += '&'.join(params)
    return url


# we permit defaults for duration and granularity, but only for the
# purpose of quick testing. it is easier to enter in the browser's url
# bar when certain values have defaults.
_one_day_s = int(datetime.timedelta(days=1).total_seconds())
_half_an_hour_s = int(datetime.timedelta(minutes=30).total_seconds())

@app.flask.route('/charts/temperature.svg', methods=('GET',))
def temperature_chart():
    names = flask.request.args.get('names')
    xsize = flask.request.args.get('xsize', type=float, default=15)
    ysize = flask.request.args.get('ysize', type=float, default=5)
    duration = flask.request.args.get('duration', type=int, default=_one_day_s)
    granularity = flask.request.args.get('granularity', type=int, default=_half_an_hour_s)

    print(flask.request.url)

    # 'names' must be list literal
    names = eval(names)

    # cm->inch
    xsize /= 2.54
    ysize /= 2.54

    samples_per_thermometer = []
    for name in names:
        samples = app.thermometer_histories[name].distill(
            granularity=granularity,
            duration=duration)
        assert len(samples) > 0
        samples_per_thermometer.append((name, samples))

    # find global oldest and youngest samples
    youngest_ts = 0 # epoch; very old
    # very young. this is the highest possible value for timestamps on
    # 32bit, aka "The Y2038 problem". still not solved on
    # raspberry/raspbian, for example.
    oldest_ts = datetime.datetime(2038, 1, 19).timestamp()
    maxnum = 0
    for _,samples in samples_per_thermometer:
        if samples[0][0] < oldest_ts:
            oldest_ts = samples[0][0]
        if samples[-1][0] > youngest_ts:
            youngest_ts = samples[-1][0]
        if len(samples) > maxnum:
            maxnum = len(samples)

    # spline-interpolate and transform onto same time axis.
    uniform_timeaxis = numpy.linspace(oldest_ts, youngest_ts, duration/granularity)
    for _,samples in samples_per_thermometer:
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

    do_legend = len(names)>1 and True or False

    with mplutil.plot(xlim=(oldest_ts, youngest_ts), ylim=(0,100), size_inches=(xsize,ysize)):
        for name, samples in samples_per_thermometer:
            mplutil.plot_samples(samples, label=name)

        return flask.send_file(
            mplutil.as_svg_io(legend=do_legend),
            mimetype='image/svg+xml')
