# -----------------------------------------------------------
# JRAVIS WORKER — FINAL STABLE VERSION
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# FIX PYTHON PATH
# -----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

print("🔧 Adding SRC path:", SRC_DIR)
sys.path.append(SRC_DIR)

# -----------------------------------------------------------
# IMPORT ENGINE
# -----------------------------------------------------------
from unified_engine import run_all_streams_micro_engine


# -----------------------------------------------------------
# REQUIRED FOLDERS
# -----------------------------------------------------------
REQUIRED_FOLDERS = ["funnels", "factory_output"]

for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)


# -----------------------------------------------------------
# BACKEND URL
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")


# -----------------------------------------------------------
# API CALL HELPERS
# -----------------------------------------------------------
def backend_post(path, payload=None):
    headers = {"X-API-KEY": WORKER_KEY}
    url = f"{BACKEND}{path}"

    try:
        r = requests.post(url, json=payload, headers=headers)
        return r.json()
    except Exception as e:
        print("[API ERROR]", e)
        return None


# -----------------------------------------------------------
# 1) Generate Template
# -----------------------------------------------------------
def generate_template():
    print("[Factory] Generating template...")
    return backend_post("/api/factory/generate")


# -----------------------------------------------------------
# 2) Scale Variants
# -----------------------------------------------------------
def scale_template(name):
    count = random.randint(2, 5)
    return backend_post("/api/factory/scale", {"base": name, "count": count})


# -----------------------------------------------------------
# 3) Growth Evaluation
# -----------------------------------------------------------
def evaluate_growth(template_name):
    payload = {
        "template": template_name,
        "clicks": random.randint(30, 400),
        "sales": random.randint(0, 20),
        "trend": round(random.uniform(0.8, 1.6), 2)
    }
    r = backend_post("/api/growth/evaluate", payload)
    print("[Growth]", r)
    return r


# -----------------------------------------------------------
# 4) Full Cycle
# -----------------------------------------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # Step 1: Generate
    gen = generate_template()
    if not gen or "name" not in gen:
        print("❌ Template generation failed.")
        return

    name = gen["name"]
    zip_path = gen["zip"]

    # Step 2: Growth evaluation
    score = evaluate_growth(name)

    # Step 3: Scale if needed
    if score.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal Scale")
        scale_template(name)

    # Step 4: Monetize
    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name, BACKEND)


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    while True:
        run_cycle()
        print("💤 Sleeping 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    main()
