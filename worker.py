# -----------------------------------------------------------
# JRAVIS WORKER — FINAL VERSION WITH API KEY FIX
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# Ensure src is in path
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    print("🔧 Adding SRC path:", SRC_PATH)
    sys.path.append(SRC_PATH)

from unified_engine import run_all_streams_micro_engine

# Backend URL + Worker API Key
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

HEADERS = {
    "X-API-KEY": WORKER_KEY,
    "Content-Type": "application/json"
}

# Ensure folders exist
for folder in ["funnels", "factory_output"]:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# ------------------------------------------------------
# GENERATE TEMPLATE
# ------------------------------------------------------
def generate_template():
    print("[Factory] Generating template...")
    try:
        res = requests.post(
            f"{BACKEND}/api/factory/generate",
            headers=HEADERS
        )
        print("[Factory] Response:", res.json())
        return res.json()
    except Exception as e:
        print("[Factory ERROR]:", e)
        return None


# ------------------------------------------------------
# SCALE TEMPLATE
# ------------------------------------------------------
def scale_template(name):
    print("[Factory] Scaling:", name)
    try:
        payload = {"base": name, "count": random.randint(2, 6)}

        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json=payload,
            headers=HEADERS
        )
        print("[Factory] Scaled:", res.json())
        return res.json()
    except Exception as e:
        print("[Scale ERROR]:", e)
        return None


# ------------------------------------------------------
# GROWTH SCORE
# ------------------------------------------------------
def score_template(name):
    try:
        payload = {
            "template": name,
            "clicks": random.randint(20, 200),
            "sales": random.randint(0, 15),
            "trend": round(random.uniform(0.8, 1.4), 2)
        }

        res = requests.post(
            f"{BACKEND}/api/growth/evaluate",
            json=payload,
            headers=HEADERS
        )
        data = res.json()
        print("[Growth] Score:", data)
        return data
    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# MAIN CYCLE
# ------------------------------------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # 1. Generate Template
    gen = generate_template()
    if not gen or "name" not in gen:
        print("❌ Template generation failed.")
        time.sleep(3)
        return

    name = gen["name"]
    zip_path = gen["zip"]

    # 2. Growth Score
    score = score_template(name)
    if not score:
        print("⚠ Growth score failed — continuing normal scale")
        scale_template(name)
    else:
        if score.get("winner"):
            print("[Growth] WINNER → DOUBLE SCALE")
            scale_template(name)
            scale_template(name)
        else:
            print("[Growth] Normal Scale")
            scale_template(name)

    # 3. Monetization
    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name)


# ------------------------------------------------------
# ENTRY
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    while True:
        run_cycle()
        time.sleep(3)


if __name__ == "__main__":
    main()
