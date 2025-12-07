# -----------------------------------------------------------
# JRAVIS WORKER — FULL AUTOMATION MODE (FINAL FIXED VERSION)
# -----------------------------------------------------------

import os
import time
import random
import requests

from unified_engine import run_all_streams_micro_engine


# -----------------------------------------------------------
# BACKEND URL
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_API_KEY = os.getenv("WORKER_API_KEY", "")

HEADERS = {"X-API-KEY": WORKER_API_KEY}


# -----------------------------------------------------------
# 1) Generate Template ZIP  (FIXED ROUTE)
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating template...")
    try:
        res = requests.post(
            f"{BACKEND}/factory/generate",
            headers=HEADERS
        ).json()

        print("[Factory] Response:", res)
        return res

    except Exception as e:
        print("[Factory ERROR]:", e)
        return None


# -----------------------------------------------------------
# 2) Scale Template Variants  (FIXED ROUTE)
# -----------------------------------------------------------
def scale_template(base_name):
    print(f"[Factory] Scaling: {base_name}")
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/factory/scale",
            json={"base": base_name, "count": count},
            headers=HEADERS
        ).json()

        print("[Factory] Scaled:", res)
        return res

    except Exception as e:
        print("[Factory ERROR]:", e)
        return None


# -----------------------------------------------------------
# 3) Growth Engine — Score Winners
# -----------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }

        res = requests.post(
            f"{BACKEND}/api/growth/evaluate",
            json=perf,
            headers=HEADERS
        ).json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# -----------------------------------------------------------
# 4) JRAVIS Full Automation Cycle
# -----------------------------------------------------------
def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE (DEBUG)")
    print("--------------------------------------")

    # STEP 1 — Generate
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed")
        time.sleep(3)
        return

    template_name = template["name"]
    zip_path = template.get("zip")
    print(f"⚡ Template Name: {template_name}")

    # STEP 2 — Growth
    growth = evaluate_growth(template_name)

    # STEP 3 — Scale
    if growth and growth.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(template_name)
        scale_template(template_name)
    else:
        print("[Growth] Normal Scale")
        scale_template(template_name)

    # STEP 4 — Monetize
    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, template_name)

    time.sleep(3)


# -----------------------------------------------------------
# ENTRY POINT
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FULL AUTOMATION MODE ENABLED\n")

    while True:
        run_cycle()


if __name__ == "__main__":
    main()
