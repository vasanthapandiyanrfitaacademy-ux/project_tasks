from prometheus_client import Counter, Gauge, start_http_server, REGISTRY

# Prevent duplicate metrics (Streamlit reload fix)
def get_metric(name, metric):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric

# Start metrics server
try:
    start_http_server(8000)
except:
    pass

# Login metrics
login_success = get_metric("login_success_total", Counter("login_success_total", "Successful logins"))
login_failure = get_metric("login_failure_total", Counter("login_failure_total", "Failed logins"))
active_users = get_metric("active_users", Gauge("active_users", "Active users"))

# Dataset metrics
file_upload_total = get_metric("file_upload_total", Counter("file_upload_total", "File uploads"))
preprocess_total = get_metric("preprocess_total", Counter("preprocess_total", "Preprocessing runs"))
dataset_rows = get_metric("dataset_rows", Gauge("dataset_rows", "Dataset rows"))