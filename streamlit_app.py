import streamlit as st
from prometheus_client import Counter, Gauge, generate_latest

# ---------------- METRICS ----------------
login_success = Counter("login_success_total", "Successful logins")
login_failure = Counter("login_failure_total", "Failed logins")
active_users = Gauge("active_users", "Active users")

users = {
    "vasanth": "123",
    "admin": "admin"
}

st.title("Pharmalytics Login")

u = st.text_input("Username")
p = st.text_input("Password", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Login"):

    if u in users and users[u] == p:
        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True
        st.success("Login Success")
    else:
        login_failure.inc()
        st.error("Login Failed")

# Debug metrics view
if st.sidebar.button("Show Metrics"):
    st.code(generate_latest().decode("utf-8"))