"""Diary Sentiment Analyzer

Prerequisites (from terminal, within your virtual‑env):
    pip install streamlit nltk

Run the app:
    streamlit run main.py

This script scans the local **diary** folder for daily files named
`YYYY-MM-dd.txt`, evaluates each entry with VADER (NLTK) sentiment analysis
and produces two **line charts** via Streamlit:
    • Positivity score per day
    • Negativity score per day (labelled *neg*)

NOTE on terminology – il requisito originale chiama il secondo dizionario
``dict_neu`` ma contiene i punteggi di **negatività**. Mantengo il nome
per aderire alla specifica; puoi rinominarlo in ``dict_neg`` se preferisci.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import nltk
import pandas as pd
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer

# ---------------------------------------------------------------------------
# 1. Ensure VADER resources are available
# ---------------------------------------------------------------------------
# (download silently the first time – runs quickly and is cached afterwards)
nltk.download("vader_lexicon", quiet=True)

# ---------------------------------------------------------------------------
# 2. Initialise analyzers and data-structures
# ---------------------------------------------------------------------------
SIA = SentimentIntensityAnalyzer()

dict_pos: dict[str, float] = {}
# Spec name is "dict_neu" even though it will store **negativity** values.
dict_neu: dict[str, float] = {}

# Path to the "diary" folder located alongside this file
DATA_DIR = Path(__file__).with_name("diary")
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}\.txt$")

# ---------------------------------------------------------------------------
# 3. Scan diary entries and populate dict_pos / dict_neu
# ---------------------------------------------------------------------------
for entry in sorted(DATA_DIR.glob("*.txt")):
    if not DATE_RX.match(entry.name):
        # Skip files not matching the expected date pattern
        continue

    text = entry.read_text(encoding="utf-8", errors="ignore")
    scores = SIA.polarity_scores(text)

    stem = entry.stem  # filename without extension, e.g. "2023-10-24"
    dict_pos[stem] = scores["pos"]          # positivity (0‑1)
    dict_neu[stem] = scores["neg"]          # negativity (0‑1)

# ---------------------------------------------------------------------------
# 4. Prepare a tidy DataFrame for visualisation
# ---------------------------------------------------------------------------
if not dict_pos:
    st.warning("No diary entries were found in the expected format.")
    st.stop()

# Sort chronologically based on the date string keys
ordered_keys = sorted(dict_pos.keys())

df = pd.DataFrame(
    {
        "date": ordered_keys,
        "positivity": [dict_pos[k] for k in ordered_keys],
        "negativity": [dict_neu[k] for k in ordered_keys],
    }
).set_index("date")

# ---------------------------------------------------------------------------
# 5. Streamlit UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Diary Sentiment Analysis", layout="centered")

st.title("📖 Diary Sentiment Analysis")

st.markdown(
    "Questo cruscotto mostra i punteggi di **positività** e **negatività** "
    "per ciascun diario (calcolati con NLTK VADER)."
)

# --- Line charts stacked vertically ----------------------------------------

st.subheader("Positivity per Day")
st.line_chart(df["positivity"], use_container_width=True)

st.subheader("Negativity per Day")
st.line_chart(df["negativity"], use_container_width=True)

# ---------------------------------------------------------------------------
# 6. Display raw data (optional)
# ---------------------------------------------------------------------------
with st.expander("Show raw sentiment scores"):
    st.dataframe(df, use_container_width=True)
