#!/usr/bin/env python3
"""
A simple Flask application that serves a welcome page.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    """
    Home route that renders the index.html template.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    """
    Run the Flask application in debug mode.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
