# File: src/app/__init__.py
import os
from flask import Flask
from argon2 import PasswordHasher
from psycopg import IntegrityError
from .models import User, db

ph = PasswordHasher()


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

        admin_email = os.environ.get("DEFAULT_ADMIN_EMAIL")
        admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD")

        if admin_email and admin_password:
            if not User.query.filter_by(email=admin_email).first():
                try:
                    hashed_password = ph.hash(admin_password)
                    admin = User(
                        email=admin_email, password=hashed_password, role="ADMIN"
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print(f"Success: Default admin {admin_email} initialised.")
                except IntegrityError:
                    # Catch the error if another worker created the admin a millisecond before this one
                    db.session.rollback()
                    print(
                        f"Notice: Admin {admin_email} was already created by another worker."
                    )
        else:
            print(
                "Notice: Admin credentials not found in environment. Skipping creation."
            )

    return app
