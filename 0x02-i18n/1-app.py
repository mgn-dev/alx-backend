#!/usr/bin/env python3
"""
1-app.py

A simple Flask application that serves a home page using Flask-Babel for
internationalization.

This application supports English and French languages and runs on host
0.0.0.0 at port 5000.
"""

from flask_babel import Babel
from flask import Flask, render_template


class Config:
    """Represents the configuration settings for Flask-Babel.

    Attributes:
        LANGUAGES (list): A list of supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): The default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): The default timezone for the application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@app.route('/')
def get_index() -> str:
    """Render the home/index page.

    Returns:
        str: The rendered template for the home page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    """Run the Flask application on host 0.0.0.0 and port 5000.

    This will make the app accessible to all network interfaces.
    """
    app.run(host='0.0.0.0', port=5000)
