#!/usr/bin/python3
"""
This module starts a flask web application and displays all states from
a database
"""


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states():
    """
    Lists all states present in the database
    """
    states = storage.all(State)
    sorted_states = dict(sorted(states.items(), key=lambda item: item[1].name))
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    Responsible for clean up e.g closing db connections
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
