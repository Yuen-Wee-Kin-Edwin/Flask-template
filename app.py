from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


@app.route("/")
def index():
    name = "Edwin"
    return render_template("index.html", person=name)


@app.route("/about")
def about():
    return "<p>About, World!!!!!</p>"
