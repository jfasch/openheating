from .instance import app
from .history_utils import make_histogram_input__full_label
from . import svg

from ..base.history import History

from flask import request

import datetime


@app.flask.route('/thermometers/<name>')
def thermometer(name):
    return app.render_template(
        'thermometer.html',
        name = name,
        # is there a better way to augment jinja2 templates with
        # functions and/or modules? other than pass them?
        svg = svg,
        datetime = datetime,
    )
