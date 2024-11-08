#!/usr/bin/env python3
"""A Basic Flask application with internationalization support.

This application serves a home page and retrieves the user's preferred
language using Flask-Babel. It supports English and French languages
and runs on host 0.0.0.0 at port 5000.
"""

from flask import Flask, request, render_template
from flask_babel import Babel

# Create and configure the Flask app
app = Flask(__name__)
babel = Babel(app)

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

app.config.from_object(Config)
app.url_map.strict_slashes = False

# @babel.localeselector
def get_locale() -> str:
    """Retrieve the best matching locale from the request headers.

    Returns:
        str: The best matched language from the accept languages.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """Render the home/index page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    """Run the Flask application on host 0.0.0.0 and port 5000.

    This makes the app accessible to all network interfaces.
    """
    app.run(host='0.0.0.0', port=5000)
