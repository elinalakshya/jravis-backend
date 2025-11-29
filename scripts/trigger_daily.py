import requests

BACKEND = "https://jravis-backend.onrender.com"

def trigger():
    url = f"{BACKEND}/report/daily/trigger"
    r = requests.post(url)
    print("[trigger_daily] Calling JRAVIS backend...")
    print("[trigger_daily]", r.status_code, "-", r.text)

if __name__ == "__main__":
    trigger()
