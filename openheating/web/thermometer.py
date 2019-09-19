from .instance import app
from .history_utils import make_histogram_input__full_label

import datetime


@app.flask.route('/thermometers/<name>')
def thermometer(name):
    thermometer = app.thermometers[name]
    history = app.thermometer_histories[name]

    return app.render_template(
        'thermometer.html',
        thermometer = thermometer,
        decision_samples = make_histogram_input__full_label(history.distill(
            granularity=1,
            duration=30)),
        hour_samples = make_histogram_input__full_label(history.distill(
            granularity=datetime.timedelta(minutes=1),
            duration=datetime.timedelta(hours=1))),
        day_samples = make_histogram_input__full_label(history.distill(
            granularity=datetime.timedelta(minutes=10),
            duration=datetime.timedelta(days=1)))
    )
