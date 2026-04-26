# File: src/app/__init__.py
import os
from flask import Flask
from .models import db


def create_app():
    # Initialise the core FLask application.
    app = Flask(__name__)

    # Configure the secret key required for flash messages and session management.
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "Critical Error: DATABASE_URL is not set. Check environment configuration."
        )
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    db.init_app(app)

    # Register blueprints for route management.
    from .routes import main_bp, auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Generate tables automatically if they do not exist.
    with app.app_context():
        db.create_all()

    return app
