import streamlit as st
from time import sleep
import pandas as pd

# ✅ import metrics (IMPORTANT)
from metrics import (
    login_success, login_failure, active_users,
    file_upload_total, preprocess_total, dataset_rows
)

st.title("Pharmalytics Login")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username == "guest" and password == "guest123":

        if not st.session_state.logged_in:
            login_success.inc()
            active_users.inc()
            st.session_state.logged_in = True

        st.success("Login successful")
        sleep(1)

    else:
        login_failure.inc()
        st.error("Invalid credentials")


# ---------------- FILE UPLOAD ----------------
st.header("Upload Dataset")

file = st.file_uploader("Upload CSV", type="csv")

if file:
    df = pd.read_csv(file)

    # Metrics
    file_upload_total.inc()
    dataset_rows.set(len(df))

    st.write(df)

    if st.button("Preprocess"):
        df = df.dropna()

        preprocess_total.inc()
        dataset_rows.set(len(df))

        st.success("Preprocessing done")
        st.write(df)