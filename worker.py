# -----------------------------------------------------------
# JRAVIS WORKER — Batch 12 Growth Optimizer + Batch 9 Factory
# -----------------------------------------------------------

import os
import time
import random
import requests

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
API_KEY = os.getenv("REPORT_API_CODE")  # Worker auth key


HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}


# ------------------------------------------------------
# Template Generator
# ------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")
    try:
        r = requests.post(f"{BACKEND}/api/factory/generate", headers=HEADERS)
        res = r.json()
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
        r = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": base_name, "count": count},
            headers=HEADERS
        )
        res = r.json()

        print("[Factory] Scaled:", res)
        return res
    except Exception as e:
        print("[Factory] ERROR scaling:", e)
        return None


# ------------------------------------------------------
# Growth Optimizer Evaluation
# ------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }

        r = requests.post(
            f"{BACKEND}/api/growth/evaluate",
            json=perf,
            headers=HEADERS
        )

        res = r.json()
        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# Worker Loop
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS Worker Started (Batch 12 Active)")

    while True:

        # Random chance to generate a new template
        if random.random() < 0.45:
            template = generate_template()

            if template and "name" in template:
                base = template["name"]

                growth = evaluate_growth(base)

                if growth and growth.get("winner"):
                    print("[Growth] WINNER → Scaling aggressively!")
                    scale_template(base)
                    scale_template(base)
                else:
                    scale_template(base)

        print("⏳ Sleeping 10 minutes...\n")
        time.sleep(600)


# ------------------------------------------------------
# Entry Point
# ------------------------------------------------------
if __name__ == "__main__":
    main()
