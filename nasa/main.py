import streamlit as st
import requests as rq
from images import get_image


nasa_url = "https://api.nasa.gov/planetary/apod?date=2025-06-01&" \
    "api_key=TZFNulnLGWpH9bB6Gi7FgHRwVHVQMb2nZMvE4UP2"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

data = rq.get(nasa_url, headers=headers)
data = data.json()
datatime = data.get("date")
description = data.get(
    "explanation") or "Nessuna descrizione disponibile."
title = data.get("title") or "nessun title"
img_url = data.get("url") or "nessuna image"


st.set_page_config(layout="centered")


# st.title(title)
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>",
            unsafe_allow_html=True)
st.text('')
# get images from Nasa
get_image(img_url)


# req = rq.get(nasa_url, headers=headers)
# content = req.json()


content2 = "image2.jpg"
st.image(content2)
st.text(description)
