# File: src/app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher
from .models import db, User

main_bp = Blueprint("main", __name__)
ph = PasswordHasher()


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Process user authentication and initialise sessions."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please provide both email and password.", "warning")
            return redirect(url_for("auth.login"))

        user = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()

        if user:
            try:
                ph.verify(user.password, password)

                if ph.check_needs_rehash(user.password):
                    user.password = ph.hash(password)
                    db.session.commit()

                session["user_id"] = user.id
                flash("Login successful.", "success")
                return redirect(url_for("main.index"))

            except VerifyMismatchError:
                pass

        flash("Invalid email or password.", "danger")
        return redirect(url_for("auth.login"))

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
            flash("All fields are mandatory.", "danger")
            return redirect(url_for("auth.signup"))

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "warning")
            return redirect(url_for("auth.signup"))

        # Secure the password using Argon2id.
        hashed_password = ph.hash(password)

        # ORM Database execution.
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)

        try:
            # Commit the transaction explicitly to save the object.
            db.session.commit()
            flash("Account successfully created. Please log in.", "success")
            return redirect(url_for("auth.login"))

        except IntegrityError:
            # Roll back the transaction if the unique constraint on the email column is violated.
            db.session.rollback()
            flash(
                "Registration failed. The email address might already be in use.",
                "danger",
            )
            return redirect(url_for("auth.signup"))

    return render_template("signup.html")
