# File: src/app/routes.py
from flask import Blueprint, render_template
from .db import get_db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the primary index page and verify the database connection."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    cursor.close()

    print(f"Connection Successful! PostgreSQL version: {db_version[0]}", flush=True)

    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    """Render the login page."""
    return render_template("login.html")


@auth_bp.route("/signup")
def signup():
    """Render the sign-up page."""
    return render_template("signup.html")
