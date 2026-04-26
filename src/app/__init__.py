# File: src/app/__init__.py
from flask import Flask
import os


def create_app():
    # Initialise the core FLask application.
    app = Flask(__name__)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "Critical Error: DATABASE_URL is not set. Check environment configuration."
        )
    app.config["DATABASE_URL"] = database_url

    # Initialise the database components.
    from . import db

    db.init_app(app)

    # Register blueprints for route management.
    from .routes import main_bp, auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
