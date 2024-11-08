#!/usr/bin/env python3
"""A Basic Flask application with internationalization support.

This application serves a home page and retrieves the user's preferred
language and timezone using Flask-Babel. It supports multiple languages
and runs on host 0.0.0.0 at port 5000.
"""

import pytz
from flask import Flask, request, render_template, g
from flask_babel import Babel
from typing import Union, Dict


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


# Create and configure the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Sample user data for demonstration
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieve a user based on the user ID from query parameters.

    Returns:
        Union[Dict, None]: The user information if found, otherwise None.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Run routines before processing each request.

    This function fetches user information and stores it in the global
    context for use during the request.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Retrieve the best matching locale for the web page.

    This function checks for a 'locale' parameter in the query string,
    user-specific locale, or the request's accepted languages.

    Returns:
        str: The best matched language based on the priority.
    """
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    """Retrieve the timezone for the web page.

    This function checks for a 'timezone' parameter in the query string,
    user-specific timezone, or returns the default timezone.

    Returns:
        str: The best matched timezone based on the priority.
    """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """Render the home/index page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    """Run the Flask application on host 0.0.0.0 and port 5000.

    This will make the app accessible to all network interfaces.
    """
    app.run(host='0.0.0.0', port=5000)
