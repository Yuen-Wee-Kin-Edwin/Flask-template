# src/config/settings.py

import os
from urllib.parse import quote_plus


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_db_password():
        secret_path = "/db/password.txt"
        if os.path.exists(secret_path):
            with open(secret_path) as f:
                return f.read().strip()
        return os.getenv("POSTGRES_PASSWORD", "password")

    @classmethod
    def init_app(cls, app):
        """Set dynamic config values like the DB URI."""
        raw_password = cls.get_db_password()
        db_user = os.getenv("POSTGRES_USER")
        db_password = quote_plus(raw_password)
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
