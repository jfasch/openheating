from .instance import app
from .history_utils import make_histogram_input__no_label

import flask

import datetime


@app.flask.route('/thermometers')
def thermometers():
    samples_per_thermometer = {}
    for name in app.thermometers.keys():
        samples_per_thermometer[name] = make_histogram_input__no_label(app.thermometer_histories[name].distill(
            granularity=datetime.timedelta(minutes=1),
            duration=datetime.timedelta(days=1)))

    return app.render_template(
        'thermometers.html', 
        samples_per_thermometer = samples_per_thermometer,
    )
