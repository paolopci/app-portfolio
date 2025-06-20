from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")  # è ka Home page
def home():
    return render_template("home.html")


@app.route("/about/api/v1/<station>/<date>")  # è la Home page
def about(station, date):
    temperature = 23
    result = {"station": station,
              "date": date,
              "temperature": temperature
              }
    return result


if __name__ == "__main__":
    app.run(debug=True)
