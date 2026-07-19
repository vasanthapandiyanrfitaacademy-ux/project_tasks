from navigation import make_sidebar
import streamlit as st
import pandas as pd
import os
from prometheus_client import Counter, Gauge, REGISTRY

# ---------------- SAFE METRIC CREATION ----------------
def get_metric(name, metric):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric

# Metrics
dataset_uploads = get_metric(
    "dataset_upload_total",
    Counter("dataset_upload_total", "Number of dataset uploads")
)

preprocess_runs = get_metric(
    "preprocess_runs_total",
    Counter("preprocess_runs_total", "Number of preprocessing executions")
)

active_users = get_metric(
    "active_users",
    Gauge("active_users", "Active users")
)

# ---------------- PREPROCESS FUNCTION ----------------
def preprocess_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    preprocess_runs.inc()  # 🔥 count preprocessing

    unnamed_columns = [col for col in dataset.columns if 'Unnamed' in col]
    dataset.drop(unnamed_columns, axis=1, inplace=True)

    dataset.replace("#REF!", None, inplace=True)
    dataset.dropna(inplace=True)

    preprocessed_dataset = dataset.reset_index(drop=True)

    preprocessed_dataset["Date Sold"] = pd.to_datetime(
        preprocessed_dataset["Date Sold"], format="%m/%d/%Y"
    )
    preprocessed_dataset = preprocessed_dataset.set_index("Date Sold")

    preprocessed_dataset["Sell Price"] = pd.to_numeric(
        preprocessed_dataset["Sell Price"], errors="coerce"
    )
    preprocessed_dataset["Sell Price"] = preprocessed_dataset["Sell Price"].round(0)

    return preprocessed_dataset


# ---------------- MAIN ----------------
def main():
    make_sidebar()

    st.title("Welcome to Pharmalytics!")

    # Ensure session
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.markdown("""
    Pharmalytics is a sales prediction system developed for FirstMed Pharmacy using the **Prophet** model.
    """)

    file = st.file_uploader("Upload Sales Dataset", type="csv")
    dataset_exists = os.path.exists("uploaded_dataset.csv")

    # ---------------- LOAD DATA ----------------
    if dataset_exists and file is None:
        dataset = pd.read_csv("uploaded_dataset.csv", index_col=None)

    elif file is None:
        st.warning("Please upload a CSV file.")
        st.stop()

    else:
        dataset = pd.read_csv(file, index_col=False)
        dataset.to_csv("uploaded_dataset.csv", index=None)

        dataset_uploads.inc()  # 🔥 count upload

    st.write("**Dataset Preview:**")
    st.dataframe(dataset, width=700)

    # ---------------- PREPROCESS ----------------
    pre_con = st.expander("Show Preprocessing Procedure")

    with pre_con:
        preprocessed_dataset = preprocess_dataset(dataset)
        preprocessed_dataset.to_csv(
            "preprocessed_dataset.csv", date_format="%m/%d/%Y"
        )

        st.subheader("Data Pre-processing")
        st.write("**Preprocessed Dataset**")
        st.dataframe(preprocessed_dataset, width=700)


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()