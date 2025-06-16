import streamlit as st
import pandas as pd

# read the CSV file
tm = pd.read_csv('team.csv', sep=',')
st.set_page_config(layout="wide")

team = st.title('The Best Company')
content = """
Welcome to our company! We are a team of dedicated professionals committed to delivering the best services and products to our clients. Our expertise spans various fields, ensuring that we can meet diverse needs with excellence and innovation.
Welcome to our company! We are a team of dedicated professionals committed to delivering the best services and products to our clients. Our expertise spans various fields, ensuring that we can meet diverse needs with excellence and innovation.
"""
st.write(content)
st.header('Our Team')

col1, col2, col3 = st.columns(3)

with col1:
    for index, row in tm[:4].iterrows():
        st.subheader(row['first name'] + ' ' + row['last name'])
        st.write(row['role'])
        st.image('photo/' + row['image'])
with col2:
    for index, row in tm[4:8].iterrows():
        st.subheader(row['first name'] + ' ' + row['last name'])
        st.write(row['role'])
        st.image('photo/' + row['image'])
with col3:
    for index, row in tm[8:12].iterrows():
        st.subheader(row['first name'] + ' ' + row['last name'])
        st.write(row['role'])
        st.image('photo/' + row['image'])
