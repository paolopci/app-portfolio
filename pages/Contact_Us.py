import streamlit as st
from send_email2 import send_email


st.header("Contact Me")

with st.form(key='email_forms'):
    user_email = st.text_input(
        "Your email address", placeholder="Enter your email")
    email_subject = st.text_input(
        "Subject", placeholder="Enter email subject")
    user_message = st.text_area(
        "Your message", height=200, placeholder="Enter your message here")
    submit_button = st.form_submit_button("Submit")
if submit_button:
    send_email(user_message, email_subject, user_email)
