from .instance import app


@app.flask.route('/switches')
def switches():
    return app.render_template(
        'switches.html', 
    )
