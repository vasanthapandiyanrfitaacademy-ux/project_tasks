from prometheus_client import Counter, Gauge, start_http_server

# Start Prometheus metrics server (http://localhost:8000/metrics)
start_http_server(8000)

# Metrics
login_success = Counter("login_success_total", "Successful logins")
login_failure = Counter("login_failure_total", "Failed logins")
active_users = Gauge("active_users", "Active users")