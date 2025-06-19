import streamlit as st
import requests as rq
from images import get_image


st.set_page_config(layout="centered")
st.title("Galaxy by the lake")

# get images from Nasa
get_image()

# contenuti
nasa_url = "https://api.nasa.gov/planetary/apod?date=2025-06-01&" \
    "api_key=TZFNulnLGWpH9bB6Gi7FgHRwVHVQMb2nZMvE4UP2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

req = rq.get(nasa_url, headers=headers)
content = req.json()

description = content.get(
    "explanation") or "Nessuna descrizione disponibile."


content2 = "image2.jpg"
st.image(content2)

st.text(description)
