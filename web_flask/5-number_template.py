#!/usr/bin/python3
"""
This module starts a Flask web application
"""


from flask import Flask, render_template


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


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Displays a number from the URL if an integer
    """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def n_template(n):
    """
    Displays an integer in the body of an HTML template
    """
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
