import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")

def trigger_daily_report():
    url = f"{BACKEND_URL}/report/daily/trigger"
    print(f"[trigger_daily] Calling JRAVIS backend at {url}...")

    try:
        response = requests.post(url)
        print("[trigger_daily] Response:", response.status_code, response.text)
    except Exception as e:
        print("[trigger_daily] ERROR:", e)


if __name__ == "__main__":
    trigger_daily_report()
