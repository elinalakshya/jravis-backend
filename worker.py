# -----------------------------------------------------------
# FIX PYTHON PATH FOR RENDER (MUST BE FIRST)
# -----------------------------------------------------------
import os
import sys

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "src")
if ENGINE_PATH not in sys.path:
    print("🔧 Adding engine path:", ENGINE_PATH)
    sys.path.append(ENGINE_PATH)

# -----------------------------------------------------------
# AUTO-CREATE REQUIRED DIRECTORIES
# -----------------------------------------------------------
REQUIRED_FOLDERS = ["funnels", "factory_output"]

for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# -----------------------------------------------------------
# IMPORT ENGINE (ONLY ONCE)
# -----------------------------------------------------------
from unified_engine import run_all_streams_micro_engine

# -----------------------------------------------------------
# JRAVIS WORKER — FULL AUTOMATION MODE
# -----------------------------------------------------------

import time
import random
import requests

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# ------------------------------------------------------
# 1) Generate Template ZIP
# ------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")
    try:
        res = requests.post(f"{BACKEND}/api/factory/generate").json()
        print("[Factory] Generated:", res)
        return res
    except Exception as e:
        print("[Factory] ERROR generating:", e)
        return None


# ------------------------------------------------------
# 2) Scale Template Variants
# ------------------------------------------------------
def scale_template(base_name):
    print(f"[Factory] Scaling: {base_name}")
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": base_name, "count": count}
        ).json()
        print("[Factory] Scaled:", res)
        return res
    except Exception as e:
        print("[Factory] ERROR scaling:", e)
        return None


# ------------------------------------------------------
# 3) Growth Engine — Score Winners
# ------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2),
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf)
        res = r.json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# 4) FULL CYCLE
# ------------------------------------------------------
def run_cycle():
    print("\n----------------------------------------")
    print("🔥 RUNNING FULL JRAVIS CYCLE")
    print("----------------------------------------")

    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed — Skipping")
        return

    base_name = template["name"]
    zip_path = template.get("zip")

    growth = evaluate_growth(base_name)

    if growth and growth.get("winner"):
        print("[Growth] WINNER — Double Scaling Mode Activated!")
        scale_template(base_name)
        scale_template(base_name)
    else:
        print("[Growth] Normal scaling")
        scale_template(base_name)

    if zip_path:
        print("\n💰 Starting Monetization Engine...")
        run_all_streams_micro_engine(zip_path, base_name)
    else:
        print("⚠️ No ZIP found — Monetization Skipped")


# ------------------------------------------------------
# 5) MAIN LOOP
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FULL AUTOMATION ENABLED")

    while True:
        run_cycle()

        for i in range(6):
            print(f"💓 Heartbeat ({i+1}/6)")
            time.sleep(100)


if __name__ == "__main__":
    main()
