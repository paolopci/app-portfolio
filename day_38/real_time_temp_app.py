"""
Streamlit dashboard per visualizzare in tempo reale le temperature registrate
nel file `data_temp.txt` (formato "date,temperature").

La struttura della data è `yy-mm-dd-HH-MM-SS`, ad es. `25-06-26-20-55-29`,
che corrisponde a 26 giugno 2025 alle 20:55:29.

Esecuzione:
    pip install streamlit streamlit-autorefresh pandas
    streamlit run real_time_temp_app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Percorso del file di log generato da service_temp.py / main_temp.py
DATA_FILE = Path(__file__).resolve().parent / "data_temp.txt"

# Intervallo di aggiornamento automatico (millisecondi)
REFRESH_INTERVAL_MS = 2_000  # 2 secondi


def read_temperature_log(path: Path) -> pd.DataFrame:
    """Legge il file CSV e restituisce un DataFrame indicizzato per datetime."""
    if not path.exists():
        # Restituisce DF vuoto con colonne previste per evitare errori
        return pd.DataFrame(columns=["temperature"], dtype=float)

    df = pd.read_csv(path)  # colonne: date,temperature

    # Converte il campo 'date' in datetime: %y-%m-%d-%H-%M-%S
    df["datetime"] = pd.to_datetime(
        df["date"],
        format="%y-%m-%d-%H-%M-%S",
        errors="coerce",
    )

    # Converte la colonna temperature in numeri (float)
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")

    # Elimina righe con parsing fallito
    df = df.dropna(subset=["datetime", "temperature"])

    # Ordina cronologicamente e imposta l'indice per il grafico
    df = df.sort_values("datetime").set_index("datetime")

    # Mantiene solo la colonna temperatura per semplificare la visualizzazione
    return df[["temperature"]]

# ----------------------------- Interfaccia Streamlit -----------------------------


st.set_page_config(
    page_title="Temperatura in tempo reale",
    layout="centered",
)

st.title("\U0001F7E2 Monitoraggio Temperatura")

# Ricarica automatica della pagina a intervalli regolari
_ = st_autorefresh(interval=REFRESH_INTERVAL_MS, key="autoreload")

# Carica i dati ad ogni esecuzione/rerun
data = read_temperature_log(DATA_FILE)

if data.empty:
    st.warning("Nessun dato disponibile nel file `data_temp.txt`.")
    st.stop()

# Disegna il grafico a linee continuo (asse x = datetime, asse y = temperatura)
st.line_chart(data, use_container_width=True)

# Mostra l'ultima lettura come metrica separata
latest_time = data.index[-1].strftime("%d/%m/%Y %H:%M:%S")
latest_temp = data["temperature"].iloc[-1]

st.metric(
    label="Ultima lettura (°C)",
    value=f"{latest_temp:.1f}",
    help=f"Rilevata il {latest_time}",
)
