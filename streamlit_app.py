import streamlit as st
from time import sleep
from prometheus_client import Counter, Gauge, start_http_server

# -------------------------------
# Start Prometheus Metrics Server
# -------------------------------
if "metrics_started" not in st.session_state:
    try:
        start_http_server(8000)
        st.session_state.metrics_started = True
    except OSError:
        # Server already running
        pass

# -------------------------------
# Prometheus Metrics
# -------------------------------
login_success = Counter(
    "login_success_total",
    "Number of successful logins"
)

login_failure = Counter(
    "login_failure_total",
    "Number of failed logins"
)

active_users = Gauge(
    "active_users",
    "Currently active users"
)

# -------------------------------
# Demo Users
# -------------------------------
users = {
    "vasanth": "123",
    "admin": "admin"
}

# -------------------------------
# Session Variables
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "success_count" not in st.session_state:
    st.session_state.success_count = 0

if "failure_count" not in st.session_state:
    st.session_state.failure_count = 0

# -------------------------------
# UI
# -------------------------------
st.title("🔐 Pharmalytics Login")

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username] == password:

            login_success.inc()
            active_users.inc()

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.success_count += 1

            st.success("✅ Login Successful")
            sleep(1)
            st.rerun()

        else:
            login_failure.inc()
            st.session_state.failure_count += 1
            st.error("❌ Invalid Username or Password")

else:

    st.success(f"Welcome {st.session_state.username}")

    if st.button("Logout"):

        active_users.dec()

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.success("Logged Out")
        sleep(1)
        st.rerun()

# -------------------------------
# Dashboard
# -------------------------------
st.divider()

st.subheader("Application Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Successful Logins",
    st.session_state.success_count
)

col2.metric(
    "Failed Logins",
    st.session_state.failure_count
)

col3.metric(
    "Active Users",
    1 if st.session_state.logged_in else 0
)

st.info("Prometheus Metrics Endpoint: http://localhost:8000/metrics")