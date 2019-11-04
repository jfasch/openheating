from .instance import app
from .history_utils import make_histogram_input__full_label

from ..base.history import History

from flask import request

import datetime


@app.flask.route('/thermometers/<name>')
def thermometer(name):
    thermometer = app.thermometers[name]

    if request.args.get('test'):
        history = History(samples=((ts,42) for ts in range(0, 60*60*24, 5)))
    else:
        history = app.thermometer_histories[name]

    decision_samples = make_histogram_input__full_label(history.distill(
        granularity=1,
        duration=30))
    hour_samples = make_histogram_input__full_label(history.distill(
        granularity=datetime.timedelta(minutes=1),
        duration=datetime.timedelta(hours=1)))
    day_samples = make_histogram_input__full_label(history.distill(
        granularity=datetime.timedelta(minutes=10),
        duration=datetime.timedelta(days=1)))

    return app.render_template(
        'thermometer.html',
        thermometer = thermometer,
        decision_samples = decision_samples,
        hour_samples = hour_samples,
        day_samples = day_samples,
    )
