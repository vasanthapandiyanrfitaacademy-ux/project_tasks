import streamlit as st
from time import sleep
from navigation import make_sidebar
from metrics import login_success, login_failure, active_users
# ---------------- UI ----------------
make_sidebar()

st.title("Welcome to Pharmalytics")
st.write("Please log in to continue (username `guest`, password `guest123`).")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------------- LOGIN ----------------
if st.button("Log in", type="primary"):

    if username == "guest" and password == "guest123":

        # Prevent double counting
        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/page1.py")

    else:
        login_failure.inc()
        st.error("Incorrect username or password")