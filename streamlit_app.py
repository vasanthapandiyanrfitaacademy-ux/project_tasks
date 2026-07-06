import streamlit as st
from time import sleep
from prometheus_client import Counter, Gauge

# ---------------- METRICS ----------------
login_success = Counter("login_success_total", "Successful logins")
login_failure = Counter("login_failure_total", "Failed logins")
active_users = Gauge("active_users", "Active users")

# ---------------- USERS ----------------
users = {
    "vasanth": "123",
    "admin": "admin"
}

st.title("Pharmalytics Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Login"):

    if username in users and users[username] == password:

        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success("Login Success")
        sleep(1)

    else:
        login_failure.inc()
        st.error("Login Failed")