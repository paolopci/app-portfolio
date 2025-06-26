import streamlit as st

# Center the header text
st.markdown("<h1 style='text-align: center;'>Contact Me</h1>",
            unsafe_allow_html=True)

# Create a container for the form
with st.container():
    # Email input field
    email = st.text_input("Your email address")

    # Message text area
    message = st.text_area("Your message", height=200)

    # Submit button aligned to the left
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        submit_button = st.button("Submit")

# Handle form submission
if submit_button:
    if email and message:
        st.success("Thank you for your message! We'll get back to you soon.")
    else:
        st.error("Please fill in all fields.")
