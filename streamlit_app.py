import streamlit as st
from time import sleep
from navigation import make_sidebar

# ✅ Prometheus
from prometheus_client import start_http_server, Counter, Gauge

start_http_server(8000)

login_success = Counter('login_success_total', 'Total successful logins')
login_failure = Counter('login_failure_total', 'Total failed logins')
active_users = Gauge('active_users', 'Currently active users')

# ✅ Multiple users (ADD HERE)
users = {
    "Vasanth": "vasu123",
    "Admin": "admin123"
}

make_sidebar()

st.title("Welcome back to Pharmalytics powered by Vasanth")

st.write("Login users:")
st.write("👉 Vasanth / vasu123")
st.write("👉 Admin / admin123")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    
    # ✅ Check user from dictionary
    if username in users and users[username] == password:
        st.session_state.logged_in = True

        login_success.inc()
        active_users.inc()

        st.success(f"Welcome {username} 🎉")
        sleep(0.5)
        st.switch_page("pages/page1.py")

    else:
        login_failure.inc()
        st.error("Incorrect username or password")