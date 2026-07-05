from prometheus_client import start_http_server
import time

if __name__ == "__main__":
    print("✅ Metrics running on 8000")

    start_http_server(8000)

    while True:
        time.sleep(5)