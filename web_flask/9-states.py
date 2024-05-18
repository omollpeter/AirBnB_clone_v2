#!/usr/bin/python3
"""
This module starts a flask web application and displays all states from
a database
"""


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """
    Lists all states present in the database
    """
    states = storage.all(State)
    sorted_states = dict(sorted(states.items(), key=lambda item: item[1].name))

    s_name = ''
    if id:
        for s in states.values():
            if s.id == id:
                s_name = s.name

    return render_template(
        '9-states.html', states=sorted_states, id=id, s_name=s_name
    )


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    Responsible for clean up e.g closing db connections
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
