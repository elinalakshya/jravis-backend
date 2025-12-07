# -----------------------------------------------------------
# JRAVIS WORKER (FINAL VERSION — MATCHED TO NEW BACKEND)
# -----------------------------------------------------------

import os
import time
import requests
import sys

# ----------------------------
# Add /src to Python path
# ----------------------------
SRC = os.path.join(os.getcwd(), "src")
if SRC not in sys.path:
    sys.path.append(SRC)

from unified_engine import run_all_streams_micro_engine


# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY", "")

print(f"🔧 BACKEND URL = {BACKEND}")
print(f"🔧 WORKER KEY = {'SET' if WORKER_KEY else 'MISSING'}")


# ----------------------------
# BACKEND API CALL HELPERS
# ----------------------------
def api_post(path: str, payload: dict = None):
    url = f"{BACKEND}{path}"
    headers = {"X-API-KEY": WORKER_KEY}

    try:
        r = requests.post(url, json=payload, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[API POST ERROR]", e)
        return None


def api_get(path: str):
    url = f"{BACKEND}{path}"
    headers = {"X-API-KEY": WORKER_KEY}

    try:
        r = requests.get(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[API GET ERROR]", e)
        return None


# ----------------------------
# PATH HELPERS
# ----------------------------
def ensure_local_folder():
    os.makedirs("factory_output", exist_ok=True)
    os.makedirs("funnels", exist_ok=True)


def download_zip_if_missing(zip_path: str):
    """Downloads ZIP from backend if local file doesn't exist."""

    if os.path.exists(zip_path):
        return True  # Already exists

    url = f"{BACKEND}/files/{zip_path}"
    print(f"[DOWNLOAD] Trying: {url}")

    try:
        r = requests.get(url)
        if r.status_code != 200:
            print("[DOWNLOAD ERROR]", r.text)
            return False

        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

        with open(zip_path, "wb") as f:
            f.write(r.content)

        print("[DOWNLOAD] ZIP saved locally.")
        return True

    except Exception as e:
        print("[DOWNLOAD EXCEPTION]", e)
        return False


# ----------------------------
# CORE WORKER LOOP
# ----------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # 1) REQUEST NEW TEMPLATE
    task = api_post("/api/factory/generate")
    if not task or "name" not in task:
        print("❌ Template generation failed")
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory] Response:", task)

    # Ensure ZIP exists (download if needed)
    if not download_zip_if_missing(zip_path):
        print("❌ ZIP missing — cannot continue")
        return

    # 2) GROWTH EVALUATION
    score = api_post("/api/growth/evaluate", {"name": name})
    print("[Growth] Evaluation:", score)

    if not score:
        print("❌ Growth evaluation failed — skipping scaling")
        return

    # 3) SCALING LOGIC
    if score.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        api_post(f"/api/factory/scale/{name}")
        api_post(f"/api/factory/scale/{name}")
    else:
        print("[Growth] Normal Scale")
        api_post(f"/api/factory/scale/{name}")

    # 4) MONETIZATION ENGINE
    print("💰 Monetizing...")
    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)


# ----------------------------
# MAIN
# ----------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")
    ensure_local_folder()

    while True:
        run_cycle()
        time.sleep(2)


if __name__ == "__main__":
    main()
