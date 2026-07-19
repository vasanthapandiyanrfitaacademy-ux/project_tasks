import streamlit as st
from time import sleep

# ✅ import metrics (this starts server)
from metrics import login_success, login_failure, active_users

st.title("Pharmalytics Login")

# Session handling
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username == "guest" and password == "guest123":

        # Prevent double count
        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success("Login successful")
        sleep(1)
        st.switch_page("pages/page1.py")

    else:
        login_failure.inc()
        st.error("Invalid credentials")