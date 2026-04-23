# File: __init__.py
from flask import Flask, render_template


def create_app():
    # Initialise the core FLask application.
    app = Flask(__name__)

    # Define the main index route.
    @app.route("/")
    def index():
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
