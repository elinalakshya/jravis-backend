import requests

BACKEND = "https://jravis-backend.onrender.com"

def trigger():
    url = f"{BACKEND}/report/daily/trigger"
    print("[trigger_daily] Calling JRAVIS backend...")

    r = requests.post(url)

    print(f"[trigger_daily] HTTP {r.status_code} - {r.text}")

if __name__ == "__main__":
    trigger()
