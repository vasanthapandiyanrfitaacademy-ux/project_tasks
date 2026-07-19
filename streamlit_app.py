import streamlit as st
from prometheus_client import Counter, Gauge, start_http_server

# Start Prometheus server only once
if "metrics_started" not in st.session_state:
    try:
        start_http_server(8000)
    except OSError:
        # Already started
        pass
    st.session_state.metrics_started = True

# Create metrics only once
if "metrics_created" not in st.session_state:
    st.session_state.login_success = Counter(
        "login_success_total",
        "Total successful logins"
    )

    st.session_state.login_failure = Counter(
        "login_failure_total",
        "Total failed logins"
    )

    st.session_state.active_users = Gauge(
        "active_users",
        "Current active users"
    )

    st.session_state.metrics_created = True

login_success = st.session_state.login_success
login_failure = st.session_state.login_failure
active_users = st.session_state.active_users

users = {
    "vasanth": "123",
    "admin": "admin123"
}

st.title("Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username in users and users[username] == password:

        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success("Login Success")

    else:
        login_failure.inc()
        st.error("Login Failed")

if st.session_state.logged_in:
    if st.button("Logout"):
        active_users.dec()
        st.session_state.logged_in = False
        st.success("Logged out")