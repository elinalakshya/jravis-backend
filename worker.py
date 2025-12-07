import os
import time
import requests

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
KEY = os.getenv("WORKER_API_KEY", "JRAVIS_2040_MASTER_KEY")

def api_post(path):
    url = f"{BACKEND}{path}"
    r = requests.post(url, headers={"X-API-KEY": KEY})
    return r.json()

def api_get(path):
    url = f"{BACKEND}{path}"
    r = requests.get(url, headers={"X-API-KEY": KEY})
    return r.json()

def download_zip(zip_path):
    url = f"{BACKEND}/files/{zip_path}"
    os.makedirs("factory_output", exist_ok=True)
    r = requests.get(url)
    if r.status_code == 200:
        full_path = f"./{zip_path}"
        with open(full_path, "wb") as f:
            f.write(r.content)
        return full_path
    return None

def run_cycle():
    print("\n🔥 RUNNING CYCLE")

    task = api_post("/api/factory/generate")
    name = task["name"]
    zip_rel = task["zip"]

    print("[Factory]", task)

    growth = api_get(f"/api/growth/evaluate/{name}")
    print("[Growth]", growth)

    api_post(f"/api/factory/scale/{name}")

    print("💾 Downloading ZIP…")
    downloaded = download_zip(zip_rel)
    print("ZIP:", downloaded)

    print("💰 Monetization complete (simulated)")

def main():
    print("🚀 WORKER ONLINE")
    while True:
        run_cycle()
        time.sleep(3)

if __name__ == "__main__":
    main()
