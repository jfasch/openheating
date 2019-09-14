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
        decision_samples = make_histogram_input__full_label(history.decision_history()),
        hour_samples = make_histogram_input__full_label(history.hour_history()),
        day_samples = make_histogram_input__full_label(history.day_history()),
    )
