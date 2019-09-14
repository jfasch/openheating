from .instance import app
from .history_utils import make_histogram_input__no_label

import flask


@app.flask.route('/thermometers')
def thermometers():
    samples_per_thermometer = {}
    for name in app.thermometers.keys():
        samples_per_thermometer[name] = make_histogram_input__no_label(app.thermometer_histories[name].day_history())

    return app.render_template(
        'thermometers.html', 
        samples_per_thermometer = samples_per_thermometer,
    )
