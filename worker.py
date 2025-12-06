# -----------------------------------------------------------
# JRAVIS WORKER — Phase-1 Full Automation Engine
# Generates → Evaluates → Scales → Uploads → Promotes
# -----------------------------------------------------------

import os
import time
import random
import requests

from src.unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# ------------------------------------------------------
# Template Generator
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
# Scale Variants
# ------------------------------------------------------
def scale_template(base_name):
    print("[Factory] Scaling:", base_name)
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
# Growth Optimization
# ------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf)
        res = r.json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# MAIN WORKER LOOP
# ------------------------------------------------------
def run_cycle():
    print("----------------------------------------")
    print("🔥 Running 1 full cycle...")
    print("----------------------------------------")

    # -----------------------------
    # 1. Generate Base Template
    # -----------------------------
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed — skipping this cycle")
        return

    base_name = template["name"]
    zip_path = template.get("zip")

    # -----------------------------
    # 2. Growth Scoring
    # -----------------------------
    growth = evaluate_growth(base_name)

    # -----------------------------
    # 3. Scaling
    # -----------------------------
    if growth and growth.get("winner"):
        print("[Growth] WINNER → Scaling aggressively!")
        scale_template(base_name)
        scale_template(base_name)  # double-scale winners
    else:
        print("[Growth] Normal scaling...")
        scale_template(base_name)

    # -----------------------------
    # 4. Run Monetization Pipeline
    # -----------------------------
    if zip_path:
        print("\n💰 Triggering Monetization Engine...")
        run_all_streams_micro_engine(zip_path, base_name)
    else:
        print("⚠️ No ZIP found — skipping monetization")


# ------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS Worker Started — FULL AUTOMATION MODE")

    while True:
        run_cycle()

        # Heartbeat cycle (10 minutes)
        for i in range(6):
            print(f"💓 Heartbeat... ({i+1}/6)")
            time.sleep(100)  # 100 sec × 6 = 600 sec ≈ 10 min


if __name__ == "__main__":
    main()
