from prometheus_client import start_http_server, Counter, Gauge
import time

login_success = Counter("login_success_total", "Successful logins")
login_failure = Counter("login_failure_total", "Failed logins")
active_users = Gauge("active_users", "Active users")

start_http_server(8000)

print("Metrics server running on 8000")

while True:
    time.sleep(5)