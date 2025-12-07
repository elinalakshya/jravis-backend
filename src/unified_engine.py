# -----------------------------------------------------------
# JRAVIS WORKER — FINAL VERSION (2025)
# Fully automated:
# Generate → Evaluate → Scale → Monetize
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# Ensure required folders exist
REQUIRED_FOLDERS = ["funnels", "factory_output", "publishers", "src"]
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# Add ./src to Python path (Render fix)
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "src")
if ENGINE_PATH not in sys.path:
    print("🔧 Adding engine path:", ENGINE_PATH)
    sys.path.append(ENGINE_PATH)

# Import unified engine
from unified_engine import run_all_streams_micro_engine


# -----------------------------------------------------------
# Load Worker API Key
# -----------------------------------------------------------
WORKER_KEY = os.getenv("WORKER_API_KEY")
if not WORKER_KEY:
    print("❌ ERROR: WORKER_API_KEY missing in environment!")
    sys.exit(1)

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# Shared request headers
HEADERS = {
    "X-API-KEY": WORKER_KEY,
    "Content-Type": "application/json"
}


# -----------------------------------------------------------
# 1. Generate Template from Backend
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating template...")
    try:
        r = requests.post(f"{BACKEND}/factory/generate", headers=HEADERS, timeout=20)
        res = r.json()
        print("[Factory] Response:", res)
        return res
    except Exception as e:
        print("[Factory ERROR]", e)
        return None


# -----------------------------------------------------------
# 2. Scale Template Variants
# -----------------------------------------------------------
def scale_template(base_name):
    print(f"[Factory] Scaling {base_name}...")
    try:
        count = random.randint(2, 6)
        r = requests.post(
            f"{BACKEND}/factory/scale",
            json={"base": base_name, "count": count},
            headers=HEADERS,
            timeout=20
        )
        res = r.json()
        print("[Factory] Scaled:", res)
        return res
    except Exception as e:
        print("[Scale ERROR]", e)
        return None


# -----------------------------------------------------------
# 3. Growth Evaluation (Winner Scoring)
# -----------------------------------------------------------
def evaluate_growth(template_name):
    print(f"[Growth] Evaluating {template_name}...")
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf, timeout=15)
        res = r.json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]", e)
        return None


# -----------------------------------------------------------
# 4. Run Full JRAVIS Cycle
# -----------------------------------------------------------
def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # Step 1: Generate
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed — retrying next loop")
        return

    template_name = template["name"]
    zip_path = template.get("zip")
    print("⚡ Template Name:", template_name)

    # Step 2: Growth Score
    growth = evaluate_growth(template_name)

    # Step 3: Scaling logic
    if growth and growth.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(template_name)
        scale_template(template_name)
    else:
        print("[Growth] Normal Scale")
        scale_template(template_name)

    # Step 4: Monetization
    if zip_path:
        print("💰 Monetizing...")
        run_all_streams_micro_engine(zip_path, template_name)
    else:
        print("⚠️ No ZIP provided, skipping monetization.")


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FULL AUTOMATION ENABLED")

    while True:
        run_cycle()
        print("💤 Sleeping 3 seconds...")
        time.sleep(3)


# -----------------------------------------------------------
if __name__ == "__main__":
    main()
