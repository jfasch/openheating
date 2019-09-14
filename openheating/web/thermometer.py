from .instance import app

import datetime


@app.flask.route('/thermometers/<name>')
def thermometer(name):
    thermometer = app.thermometers[name]
    history = app.thermometer_histories[name]

    decision_samples = []
    for timestamp, temperature in history.decision_history():
        decision_samples.append((str(datetime.datetime.fromtimestamp(timestamp)), temperature))
    hour_samples = []
    for timestamp, temperature in history.hour_history():
        hour_samples.append((str(datetime.datetime.fromtimestamp(timestamp)), temperature))
    day_samples = []
    for timestamp, temperature in history.day_history():
        day_samples.append((str(datetime.datetime.fromtimestamp(timestamp)), temperature))

    return app.render_template(
        'thermometer.html',
        thermometer = thermometer,
        decision_samples = decision_samples,
        hour_samples = hour_samples,
        day_samples = day_samples,
    )
