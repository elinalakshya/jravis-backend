# -----------------------------------------------------------
# JRAVIS WORKER — FINAL VERSION (Factory + Monetization)
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# ENSURE REQUIRED FOLDERS
# -----------------------------------------------------------
REQUIRED_FOLDERS = ["funnels", "factory_output", "publishers", "src"]
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# -----------------------------------------------------------
# FIX PYTHON PATH
# -----------------------------------------------------------
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    print("🔧 Adding SRC path:", SRC_PATH)
    sys.path.append(SRC_PATH)

# -----------------------------------------------------------
# IMPORT ENGINE
# -----------------------------------------------------------
from unified_engine import run_all_streams_micro_engine

# -----------------------------------------------------------
# ENVIRONMENT
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY", "")

HEADERS = {
    "X-API-KEY": WORKER_KEY,
    "Content-Type": "application/json"
}

# -----------------------------------------------------------
# 1) FACTORY — GENERATE TEMPLATE
# -----------------------------------------------------------
def generate_template():
    print("[Factory] Generating template...")

    try:
        url = f"{BACKEND}/factory/generate"   # FIXED ROUTE
        res = requests.post(url, headers=HEADERS)

        data = res.json()
        print("[Factory] Response:", data)

        return data
    except Exception as e:
        print("❌ Factory ERROR:", e)
        return None

# -----------------------------------------------------------
# 2) FACTORY — SCALE TEMPLATE
# -----------------------------------------------------------
def scale_template(name):
    print("[Factory] Scaling:", name)

    try:
        count = random.randint(2, 6)

        url = f"{BACKEND}/factory/scale"      # FIXED ROUTE
        res = requests.post(
            url,
            json={"base": name, "count": count},
            headers=HEADERS
        )

        data = res.json()
        print("[Factory] Scaled:", data)

        return data
    except Exception as e:
        print("❌ Scale ERROR:", e)
        return None

# -----------------------------------------------------------
# 3) GROWTH ENGINE (LOCAL RANDOM SCORING)
# -----------------------------------------------------------
def growth_score(name):
    score = round(random.uniform(20, 180), 3)

    result = {
        "template": name,
        "score": score,
        "winner": score > 120,     # Winner threshold
        "action": "scale" if score > 120 else "pause"
    }

    print("[Growth] Evaluation:", result)
    return result

# -----------------------------------------------------------
# 4) FULL JRAVIS CYCLE
# -----------------------------------------------------------
def run_cycle():
    print("🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # ---- STEP 1: GENERATE TEMPLATE ----
    tpl = generate_template()
    if not tpl or "name" not in tpl:
        print("❌ Template generation failed.")
        return

    name = tpl["name"]
    zip_path = tpl["zip"]

    # ---- STEP 2: SCORE GROWTH ----
    score = growth_score(name)

    # ---- STEP 3: SCALING ----
    if score["winner"]:
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal Scale")
        scale_template(name)

    # ---- STEP 4: MONETIZATION ----
    print("💰 Monetizing...")

    try:
        run_all_streams_micro_engine(zip_path, name)
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)

# -----------------------------------------------------------
# 5) MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    while True:
        run_cycle()
        time.sleep(3)

# -----------------------------------------------------------
if __name__ == "__main__":
    main()
