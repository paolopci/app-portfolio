import streamlit as st
import plotly.express as px
import pandas as pd

# leggo tutti i dati
df = pd.read_csv("happy.csv")
df = df[['happiness', 'gdp', 'generosity']]
happy = df['happiness']
gdp = df['gdp']
generosity = df['generosity']

st.title = ("In search for Happiness")

option_x = (st.selectbox("Select the data for the X-axis",
                         ("GDP", "Happiness", "Generosity"))).lower()
option_y = (st.selectbox("Select the data for the Y-axis",
                         ("GDP", "Happiness", "Generosity"))).lower()


def get_data(asse_x, asse_y):
    result_x = df[asse_x]
    result_y = df[asse_y]
    return result_x, result_y


xv, yv = get_data(option_x, option_y)

# sub title
st.subheader(f"{option_x.capitalize()} and {option_y.capitalize()}")

# plot

figure = px.scatter(x=xv, y=yv, labels={
    "x": option_x.capitalize(), "y": option_y.capitalize()})
st.plotly_chart(figure)
