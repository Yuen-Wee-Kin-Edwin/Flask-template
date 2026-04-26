# File: src/app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .models import db, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
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


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    # Handle user registration, validation, and database insertion via ORM.
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Server-Side Validation.
        if not email or not password or not confirm_password:
            flash("All fields are mandatory.")
            return redirect(url_for("auth.signup"))

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for("auth.signup"))

        # Security Configuration.
        hashed_password = generate_password_hash(password)

        # ORM Database execution.
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)

        try:
            # Commit the transaction explicitly to save the object.
            db.session.commit()
            flash("Account successfully created. Please log in.")
            return redirect(url_for("auth.login"))

        except IntegrityError:
            # Roll back the transaction if the unique constraint on the email column is violated.
            db.session.rollback()
            flash("Registration failed. The email address might already be in use.")
            return redirect(url_for("auth.signup"))

    return render_template("signup.html")
