from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
basedir = os.path.dirname(__file__)
filename = os.path.join(basedir, "data_small",
                        "stations.txt")
stations = pd.read_csv(f"{filename}", skiprows=17)
# tolgo gli spazi dalle intestazioni ma non modifico stations.txt
stations.columns = stations.columns.str.strip()


@app.route("/")  # è ka Home page
def home():
    return render_template("home.html", data=stations)


@app.route("/api/v1/<station>/<date>")  # è la Home page
def about(station, date):
    basedir = os.path.dirname(__file__)
    filename = os.path.join(basedir, "data_small",
                            f"TG_STAID{str(station).zfill(6)}.txt")
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze()/10
    filtered = df.loc[df['    DATE'] == pd.to_datetime(date), '   TG']
   # temperature = 23
    result = {"station": station,
              "date": date,
              "temperature": temperature
              }
    return result


if __name__ == "__main__":
    app.run(debug=True)
