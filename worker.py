# -----------------------------------------------------------
# JRAVIS WORKER (FINAL — backend_url FIXED + VERIFICATION LOG)
# -----------------------------------------------------------

import os
import time
import sys
import requests

# Ensure src path exists
SRC_PATH = os.path.join(os.getcwd(), "src")
sys.path.append(SRC_PATH)

print("🔧 SRC PATH =", SRC_PATH)

# Import engine
from unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

print("🔧 BACKEND =", BACKEND)


def get_task():
    url = f"{BACKEND}/api/factory/generate"
    headers = {"X-API-KEY": WORKER_KEY}
    try:
        r = requests.post(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[TASK ERROR]", e)
        return None


def scale_task(name):
    url = f"{BACKEND}/api/factory/scale/{name}"
    headers = {"X-API-KEY": WORKER_KEY}
    try:
        r = requests.post(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[SCALE ERROR]", e)
        return None


def evaluate_growth(name):
    url = f"{BACKEND}/api/growth/evaluate/{name}"
    headers = {"X-API-KEY": WORKER_KEY}
    try:
        r = requests.get(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[GROWTH ERROR]", e)
        return None


def run_cycle():
    print("🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    task = get_task()
    if not task or "name" not in task:
        print("❌ Template generation failed.")
        time.sleep(3)
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory] Response:", task)

    score = evaluate_growth(name)
    print("[Growth] Evaluation:", score)

    if score.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_task(name)
        scale_task(name)
    else:
        print("[Growth] Normal Scale")
        scale_task(name)

    print("💰 Monetizing...")
    print(f"🔧 Calling Engine: run_all_streams_micro_engine('{zip_path}', '{name}', '{BACKEND}')")

    # THE FIX — THREE ARGUMENTS
    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)


def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    os.makedirs("funnels", exist_ok=True)
    os.makedirs("factory_output", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(2)


if __name__ == "__main__":
    main()
