# File: src/app/db.py
import psycopg
from flask import current_app, g


# Define a function to get the database connection.
def get_db():
    """Establish and return a database connection."""
    if "db" not in g:
        g.db = psycopg.connect(current_app.config["DATABASE_URL"])
    return g.db


def close_db(error=None):
    """Close the database connection if it exists."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Register database teardown functions with the Flask application."""
    app.teardown_appcontext(close_db)
