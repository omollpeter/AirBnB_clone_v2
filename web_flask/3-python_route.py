#!/usr/bin/python3
"""
This module starts a Flask web application
"""


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Displays a hello message as a response
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays a message as a response
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Displays a text from the URL prefixed with C
    """
    if "_" in text:
        text = text.replace("_", " ")
    return "C " + text


@app.route('/python', defaults={"text": "is cool"}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Displays a text from the URL prefixed with Python
    """
    if "_" in text:
        text = text.replace("_", " ")
    return "Python " + text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
