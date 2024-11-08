#!/usr/bin/env python3
"""A Basic Flask application with internationalization support.

This application serves a home page and retrieves the user's preferred
language using Flask-Babel. It supports English and French languages
and runs on host 0.0.0.0 at port 5000.
"""

from flask import Flask, request
from flask_babel import Babel
from config import Config
from routes import *  # Import routes


# Create and configure the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrieve the best matching locale from the request headers.

    Returns:
        str: The best matched language from the accept languages.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


if __name__ == '__main__':
    """Run the Flask application on host 0.0.0.0 and port 5000.

    This will make the app accessible to all network interfaces.
    """
    app.run(host='0.0.0.0', port=5000)
