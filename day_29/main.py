from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")  # è ka Home page
def home():
    return render_template("home.html")


@app.route("/about/api/<station>/<date>")  # è ka Home page
def about(station, date):
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
