from .instance import app


@app.flask.route('/circuits')
def circuits():
    return app.render_template(
        'circuits.html', 
    )
