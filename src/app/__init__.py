from flask import Flask, render_template


def create_app():
    # Initialise the core FLask application.
    app = Flask(__name__)

    # Define the main index route.
    @app.route("/")
    def index():
        return render_template("index.html")

    return app
