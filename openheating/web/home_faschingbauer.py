from .instance import app


@app.flask.route('/')
def home_faschingbauer():
    return app.render_template('home_faschingbauer.html')
