from .instance import app

from flask import request


@app.flask.route('/switches', methods=['GET', 'POST'])
def switches():
    if request.method == 'POST':
        for name, switch in app.switches.items():
            state = request.form.get('{}.state'.format(name))
            if state is None:
                state = False
            switch.set_state(state)

    return app.render_template(
        'switches.html', 
    )
