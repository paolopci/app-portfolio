import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# Titolo principale
st.title("Weather Forecast for the Next Days")

# Sezione Place
st.subheader("Place:")
place = st.text_input("", value="Tirana", key="place_input")

# Sezione Forecast Days
st.subheader("Forecast Days")

# Slider per i giorni di previsione
forecast_days = st.slider(
    "",
    min_value=1,
    max_value=5,
    value=2,
    key="forecast_slider"
)

# Sezione Select data to view
st.subheader("Select data to view")
data_option = st.selectbox(
    "",
    options=["Temperature", "Humidity", "Wind Speed", "Pressure"],
    index=0
)

# Generazione dati di esempio per il grafico


def generate_weather_data(days):
    """Genera dati meteorologici di esempio"""
    # Data di partenza
    start_date = datetime(2022, 9, 30, 12, 0)

    # Genera timestamp ogni 2 ore per il numero di giorni specificato
    timestamps = []
    temperatures = []

    for day in range(days):
        for hour in range(0, 24, 2):
            current_time = start_date + timedelta(days=day, hours=hour)
            timestamps.append(current_time)

            # Simula temperature realistiche con variazioni giornaliere
            base_temp = 20
            # Variazione giornaliera
            daily_variation = 4 * np.sin(2 * np.pi * hour / 24)
            random_noise = np.random.normal(0, 1)  # Rumore casuale
            temp = base_temp + daily_variation + random_noise

            # Aggiunge alcune variazioni specifiche per replicare il pattern nell'immagine
            if day == 0:
                if hour < 12:
                    temp = 24 - (hour / 12) * 4  # Diminuisce da 24 a 20
                else:
                    temp = 20  # Rimane intorno a 20
            elif day == 1:
                if hour < 12:
                    temp = 20 + (hour / 12) * 8  # Aumenta da 20 a 28
                else:
                    temp = 28 - ((hour - 12) / 12) * \
                        11  # Diminuisce da 28 a 17

            temperatures.append(temp)

    return pd.DataFrame({
        'Date': timestamps,
        'Temperature': temperatures
    })


# Genera i dati
weather_data = generate_weather_data(forecast_days)

# Titolo del grafico dinamico
chart_title = f"{data_option} for the next {forecast_days} days in {place}"
st.subheader(chart_title)

# Creazione del grafico con Plotly
fig = go.Figure()

if data_option == "Temperature":
    y_data = weather_data['Temperature']
    y_label = "Temperature (C)"
    y_range = [15, 30]
else:
    # Per altre opzioni, genera dati casuali
    if data_option == "Humidity":
        y_data = np.random.uniform(40, 90, len(weather_data))
        y_label = "Humidity (%)"
        y_range = [30, 100]
    elif data_option == "Wind Speed":
        y_data = np.random.uniform(5, 25, len(weather_data))
        y_label = "Wind Speed (km/h)"
        y_range = [0, 30]
    else:  # Pressure
        y_data = np.random.uniform(1010, 1025, len(weather_data))
        y_label = "Pressure (hPa)"
        y_range = [1005, 1030]

fig.add_trace(go.Scatter(
    x=weather_data['Date'],
    y=y_data,
    mode='lines',
    line=dict(color='#6366f1', width=2),
    name=data_option
))

# Personalizzazione del layout del grafico
fig.update_layout(
    xaxis_title="Date",
    yaxis_title=y_label,
    yaxis=dict(range=y_range),
    showlegend=False,
    plot_bgcolor='rgba(248,249,250,0.8)',
    paper_bgcolor='white',
    font=dict(size=12),
    margin=dict(l=50, r=50, t=30, b=50),
    height=400
)

# Personalizzazione degli assi
fig.update_xaxes(
    tickformat='%H:%M\n%b %d, %Y',
    tickangle=0,
    gridcolor='rgba(0,0,0,0.1)'
)

fig.update_yaxes(
    gridcolor='rgba(0,0,0,0.1)'
)

# Mostra il grafico
st.plotly_chart(fig, use_container_width=True)

# Sezione opzionale con informazioni aggiuntive
with st.expander("📊 Weather Data Details"):
    st.write(
        f"Showing {data_option.lower()} data for {place} over the next {forecast_days} day(s)")

    # Mostra alcune statistiche
    if data_option == "Temperature":
        avg_temp = np.mean(y_data)
        max_temp = np.max(y_data)
        min_temp = np.min(y_data)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Temperature", f"{avg_temp:.1f}°C")
        with col2:
            st.metric("Maximum Temperature", f"{max_temp:.1f}°C")
        with col3:
            st.metric("Minimum Temperature", f"{min_temp:.1f}°C")

    # Tabella con i dati
    if st.checkbox("Show raw data"):
        display_data = weather_data.copy()
        display_data[data_option] = y_data
        display_data['Date'] = display_data['Date'].dt.strftime(
            '%Y-%m-%d %H:%M')
        st.dataframe(display_data[['Date', data_option]],
                     use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Weather forecast data is simulated for demonstration purposes*")
