# File: src/__init__.py
from flask import Flask, render_template, g
import os
import psycopg


def create_app():
    # Initialise the core FLask application.
    app = Flask(__name__)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "Critical Error: DATABASE_URL is not set. Check environment configuration."
        )
    app.config["DATABASE_URL"] = database_url

    # Define a function to get the database connection.
    def get_db():
        if "db" not in g:
            g.db = psycopg.connect(app.config["DATABASE_URL"])
        return g.db

    # Ensure the connection is closed when the application context ends.
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    # Define the main index route.
    @app.route("/")
    def index():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()

        print(f"Connection Successful! PostgreSQL version: {db_version[0]}", flush=True)

        return render_template("index.html")

    # Define the about route
    @app.route("/about")
    def about():
        return render_template("about.html")

    # Define the login route
    @app.route("/login")
    def login():
        return render_template("login.html")

    # Define the signup route
    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    return app
