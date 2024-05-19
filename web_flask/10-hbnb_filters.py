#!/usr/bin/python3
"""
This module starts a flask web application and displays all states from
a database
"""


from flask import Flask, render_template, url_for
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Displays a html page with filter section for AirBnB clone
    """
    states = storage.all(State)
    sort_states = dict(sorted(states.items(), key=lambda item: item[1].name))

    amenities = storage.all(Amenity)
    sort_amnts = dict(sorted(amenities.items(), key=lambda item: item[1].name))
    return render_template(
        "10-hbnb_filters.html", states=sort_states, amenities=sort_amnts
    )


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    Responsible for clean up e.g closing db connections
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
