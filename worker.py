# -----------------------------------------------------------
# JRAVIS WORKER — FINAL VERSION
# -----------------------------------------------------------

import os
import sys
import time
import requests

SRC_PATH = os.path.join(os.getcwd(), "src")
sys.path.append(SRC_PATH)

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

from unified_engine import run_all_streams_micro_engine


def get_task():
    url = f"{BACKEND}/api/factory/generate"
    r = requests.post(url, headers={"X-API-KEY": WORKER_KEY})
    return r.json() if r.status_code == 200 else None


def scale_task(name, count):
    url = f"{BACKEND}/api/factory/scale"
    payload = {"base": name, "count": count}
    r = requests.post(url, json=payload, headers={"X-API-KEY": WORKER_KEY})
    return r.json() if r.status_code == 200 else None


def evaluate_growth(name):
    url = f"{BACKEND}/api/growth/evaluate"
    payload = {"template": name}
    r = requests.post(url, json=payload, headers={"X-API-KEY": WORKER_KEY})
    return r.json() if r.status_code == 200 else None


def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    task = get_task()
    if not task or "name" not in task:
        print("❌ Template generation failed.")
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory] Response:", task)

    score = evaluate_growth(name)

    if not score or "winner" not in score:
        print("❌ Growth evaluation invalid → using default")
        score = {"winner": False}

    # scaling logic
    if score["winner"]:
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_task(name, 5)
        scale_task(name, 3)
    else:
        print("[Growth] Normal Scale")
        scale_task(name, 3)

    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name, BACKEND)


def main():
    print("🚀 JRAVIS WORKER STARTED (FINAL MODE)")

    os.makedirs("factory_output", exist_ok=True)
    os.makedirs("funnels", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(3)


if __name__ == "__main__":
    main()
