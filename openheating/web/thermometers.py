from .instance import app
from .history_utils import make_histogram_input__full_label
from . import svg

import flask

import datetime


@app.flask.route('/thermometers')
def thermometers():
    return app.render_template(
        'thermometers.html', 
        svg = svg,
        datetime = datetime,
    )
