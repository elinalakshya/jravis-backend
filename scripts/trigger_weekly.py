import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")

def trigger_weekly_report():
    url = f"{BACKEND_URL}/report/weekly/trigger"
    print(f"[trigger_weekly] Calling JRAVIS backend at {url}...")

    try:
        response = requests.post(url)
        print("[trigger_weekly] Response:", response.status_code, response.text)
    except Exception as e:
        print("[trigger_weekly] ERROR:", e)


if __name__ == "__main__":
    trigger_weekly_report()
