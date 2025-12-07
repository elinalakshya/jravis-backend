# -----------------------------------------------------------
# JRAVIS WORKER — FINAL FULL-AUTOMATION ENGINE
# Generates → Evaluates → Scales → Downloads ZIP → Monetizes
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# FIX PYTHON PATH
# -----------------------------------------------------------
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    print("🔧 Adding SRC path:", SRC_PATH)
    sys.path.append(SRC_PATH)

from unified_engine import run_all_streams_micro_engine


# -----------------------------------------------------------
# BACKEND URL
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
API_HEADERS = {
    "X-API-KEY": os.getenv("WORKER_API_KEY", "")
}


# -----------------------------------------------------------
# CREATE REQUIRED FOLDERS
# -----------------------------------------------------------
for folder in ["funnels", "factory_output"]:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)


# -----------------------------------------------------------
# 1) Generate Template ZIP
# -----------------------------------------------------------
def generate_template():
    print("[Factory] Generating template...")
    try:
        res = requests.post(
            f"{BACKEND}/api/factory/generate",
            headers=API_HEADERS
        )
        return res.json()
    except Exception as e:
        print("[Factory ERROR]", e)
        return None


# -----------------------------------------------------------
# 2) Scale Variants
# -----------------------------------------------------------
def scale_template(name):
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": name, "count": count},
            headers=API_HEADERS
        )
        return res.json()
    except Exception as e:
        print("[Scale ERROR]", e)
        return None


# -----------------------------------------------------------
# 3) Growth Scoring
# -----------------------------------------------------------
def evaluate_growth(name):
    fake_score = {
        "template": name,
        "score": round(random.uniform(20, 160), 3),
        "winner": random.choice([True, False]),
        "action": "scale"
    }
    print("[Growth] Evaluation:", fake_score)
    return fake_score


# -----------------------------------------------------------
# 4) FULL CYCLE
# -----------------------------------------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # Step 1 — Generate
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed.")
        time.sleep(3)
        return

    name = template["name"]
    zip_path = template.get("zip")
    print(f"[Factory] Response: {template}")

    # Step 2 — Growth
    score = evaluate_growth(name)

    # Step 3 — Scaling
    if score.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal Scale")
        scale_template(name)

    # Step 4 — Monetization
    print("💰 Monetizing...")

    if zip_path:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    else:
        print("⚠️ Missing ZIP path — skipping monetization")


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    while True:
        run_cycle()
        print("💤 Sleeping 3 seconds...")
        time.sleep(3)


# -----------------------------------------------------------
if __name__ == "__main__":
    main()
