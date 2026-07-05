import streamlit as st
from time import sleep
from navigation import make_sidebar

# ✅ Prometheus metrics ONLY (no server)
from prometheus_client import Counter, Gauge

login_success = Counter('login_success_total', 'Total successful logins')
login_failure = Counter('login_failure_total', 'Total failed logins')
active_users = Gauge('active_users', 'Currently active users')

users = {
    "Vasanth": "vasu123",
    "Admin": "admin123"
}

make_sidebar()

st.title("Pharmalytics Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in"):
    if username in users and users[username] == password:
        st.session_state.logged_in = True

        login_success.inc()
        active_users.inc()

        st.success(f"Welcome {username}")
        sleep(0.5)
        st.switch_page("pages/page1.py")
    else:
        login_failure.inc()
        st.error("Invalid credentials")