import streamlit as st
from prometheus_client import Counter, Gauge, start_http_server
import threading

# ---------------------------
# Start Prometheus server once
# ---------------------------
if "metrics_server_started" not in st.session_state:
    def run_metrics():
        start_http_server(8000)

    threading.Thread(target=run_metrics, daemon=True).start()
    st.session_state.metrics_server_started = True

# ---------------------------
# Create metrics only once
# ---------------------------
if "login_success_metric" not in st.session_state:
    st.session_state.login_success_metric = Counter(
        "login_success_total",
        "Total successful logins"
    )

    st.session_state.login_failure_metric = Counter(
        "login_failure_total",
        "Total failed logins"
    )

    st.session_state.active_users_metric = Gauge(
        "active_users",
        "Current active users"
    )

login_success = st.session_state.login_success_metric
login_failure = st.session_state.login_failure_metric
active_users = st.session_state.active_users_metric

# ---------------------------
# Demo users
# ---------------------------
USERS = {
    "admin": "admin",
    "vasanth": "123"
}

# ---------------------------
# Session state
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------
# UI
# ---------------------------
st.title("Pharmalytics Login")

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS and USERS[username] == password:

            login_success.inc()
            active_users.inc()

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login Successful")

        else:
            login_failure.inc()
            st.error("Invalid username or password")

else:

    st.success(f"Welcome {st.session_state.username}")

    if st.button("Logout"):
        active_users.dec()
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out")

st.markdown("---")
st.write("Prometheus Metrics:")
st.code("http://localhost:8000/metrics")