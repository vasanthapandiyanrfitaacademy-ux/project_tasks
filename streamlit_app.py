import streamlit as st
from time import sleep
from navigation import make_sidebar

from prometheus_client import Counter, Gauge, REGISTRY, start_http_server

# Start Prometheus metrics server only once
if "metrics_started" not in st.session_state:
    try:
        start_http_server(8000)
        st.session_state.metrics_started = True
    except OSError:
        pass


def get_metric(name, metric_type, description):
    try:
        if metric_type == "counter":
            return Counter(name, description)
        elif metric_type == "gauge":
            return Gauge(name, description)
    except ValueError:
        return REGISTRY._names_to_collectors[name]


# Metrics
login_success = get_metric(
    "login_success_total",
    "counter",
    "Total successful logins"
)

login_failure = get_metric(
    "login_failure_total",
    "counter",
    "Total failed logins"
)

active_users = get_metric(
    "active_users",
    "gauge",
    "Currently active users"
)

# Users
users = {
    "vasanth": "vasu123",
    "admin": "admin123"
}

make_sidebar()

st.title("Pharmalytics Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Log in"):

    if username in users and users[username] == password:

        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success(f"Welcome {username}")
        sleep(1)
        st.switch_page("pages/page1.py")

    else:
        login_failure.inc()
        st.error("Invalid credentials")