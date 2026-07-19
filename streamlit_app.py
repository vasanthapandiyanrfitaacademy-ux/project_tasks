import streamlit as st
from prometheus_client import Counter, Gauge, start_http_server, REGISTRY
import threading

# ---------------------------
# Start Prometheus server only once (global)
# ---------------------------
if "server_started" not in st.session_state:
    def start_server():
        start_http_server(8000)

    threading.Thread(target=start_server, daemon=True).start()
    st.session_state.server_started = True


# ---------------------------
# Create metrics safely (avoid duplicate error)
# ---------------------------
def get_metric(name, metric_type, desc):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, desc)


login_success = get_metric(
    "login_success_total", Counter, "Total successful logins"
)

login_failure = get_metric(
    "login_failure_total", Counter, "Total failed logins"
)

active_users = get_metric(
    "active_users", Gauge, "Current active users"
)

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

            # prevent multiple increments
            if not st.session_state.logged_in:
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

        if st.session_state.logged_in:
            active_users.dec()

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.success("Logged out")

# ---------------------------
# Debug info
# ---------------------------
st.markdown("---")
st.write("Metrics URL:")
st.code("http://YOUR-IP:8000/metrics")