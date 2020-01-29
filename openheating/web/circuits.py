from .instance import app

from flask import request


@app.flask.route('/circuits', methods=['GET', 'POST'])
def circuits():
    if request.method == 'POST':
        for name, circuit in app.circuits.items():
            active = request.form.get('{}.active'.format(name))
            if active:
                circuit.activate()
            else:
                circuit.deactivate()

    return app.render_template(
        'circuits.html', 
    )
