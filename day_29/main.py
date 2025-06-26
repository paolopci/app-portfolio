from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Determina la cartella corrente del file main.py
basedir = os.path.dirname(__file__)

# Costruisce il percorso completo al file delle stazioni
filename = os.path.join(basedir, "data_small", "stations.txt")

# Legge il file delle stazioni, ignorando le prime 17 righe di intestazioni/commenti
stations = pd.read_csv(f"{filename}", skiprows=17)

# Rimuove eventuali spazi bianchi dai nomi delle colonne
stations.columns = stations.columns.str.strip()


@app.route("/")  # Homepage dell'applicazione
def home():
    # Rende il template HTML, passando il dataframe delle stazioni come contesto
    return render_template("home.html", data=stations)


# Ritorna la temperatura per una stazione in una data specifica
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = os.path.join(basedir, "data_small",
                            f"TG_STAID{str(station).zfill(6)}.txt")

    # Legge il file dati, facendo parsing automatico della colonna '    DATE'
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])

    # Estrae la temperatura per la data specifica, dividendo per 10 per ottenere gradi Celsius
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    # Costruisce un dizionario con le informazioni richieste
    result = {
        "station": station,
        "date": date,
        "temperature": temperature
    }
    return result


# Ritorna tutti i dati di temperatura per una stazione
@app.route("/api/v1/<station>")
def all_data(station):
    filename = os.path.join(basedir, "data_small",
                            f"TG_STAID{str(station).zfill(6)}.txt")

    # Legge il file dati
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])

    # Converte l'intero dataframe in una lista di dizionari
    result = df.to_dict(orient="records")
    return result


# Ritorna tutti i dati di temperatura per una stazione in un anno
@app.route("/api/v1/yearly/<station>/<year>")
def yearly_data(station, year):
    # Costruisce il percorso del file della stazione (es. TG_STAID000010.txt)
    filename = os.path.join(basedir, "data_small",
                            f"TG_STAID{str(station).zfill(6)}.txt")

    # Legge il file saltando le righe iniziali di intestazione
    df = pd.read_csv(filename, skiprows=20)

    # Rimuove eventuali spazi dalle intestazioni delle colonne (es. '    DATE' → 'DATE')
    df.columns = df.columns.str.strip()

    # Converte la colonna 'DATE' nel tipo datetime per facilitare i filtri temporali
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')

    # Filtra solo le righe che corrispondono all'anno richiesto
    df_year = df[df['DATE'].dt.year == int(year)].copy()

    # Converte la temperatura da decimi di °C a °C (es. 45 → 4.5)
    df_year['TG'] = df_year['TG'] / 10.0

    # Converte il dataframe in una lista di dizionari (serializzabile in JSON)
    result = df_year.to_dict(orient="records")

    # Ritorna il risultato
    return result


if __name__ == "__main__":
    app.run(debug=True)
