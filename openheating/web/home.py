from .instance import app


@app.flask.route('/')
def home():
    return app.render_template('home.html')
