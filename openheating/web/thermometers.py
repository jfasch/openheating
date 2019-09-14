from .instance import app

import flask


@app.flask.route('/thermometers')
def thermometers():
    return app.render_template(
        'thermometers.html', 
    )


