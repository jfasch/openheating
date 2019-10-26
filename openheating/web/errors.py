from .instance import app

import flask


@app.flask.route('/errors')
def errors():
    return app.render_template(
        'errors.html', 
    )
