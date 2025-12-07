# -----------------------------------------------------------
# FINAL JRAVIS WORKER (STRUCTURE SAFE + ROUTE SAFE)
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# Ensure required folders exist
# -----------------------------------------------------------
for f in ["funnels", "factory_output"]:
    if not os.path.exists(f):
        os.makedirs(f, exist_ok=True)

# -----------------------------------------------------------
# Add /src to Python PATH
# -----------------------------------------------------------
ENGINE_DIR = os.path.join(os.path.dirname(__file__), "src")
sys.path.append(ENGINE_DIR)

from unified_engine import run_all_streams_micro_engine

# -----------------------------------------------------------
# Backend URL
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
API_KEY = os.getenv("REPORT_API_CODE", "")

HEADERS = {"X-API-KEY": API_KEY}

# -----------------------------------------------------------
# Factory: Generate
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating template...")
    try:
        res = requests.post(
            f"{BACKEND}/api/factory/generate",
            headers=HEADERS
        ).json()
        print("[Factory] Response:", res)
        return res
    except Exception as e:
        print("[Factory ERROR]:", e)
        return None

# -----------------------------------------------------------
# Factory: Scale
# -----------------------------------------------------------
def scale_template(base):
    try:
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            headers=HEADERS,
            json={"base": base, "count": random.randint(2, 6)}
        ).json()
        print("[Factory] Scaled:", res)
    except Exception as e:
        print("[Scale ERROR]:", e)

# -----------------------------------------------------------
# Growth: Score
# -----------------------------------------------------------
def growth_score(name):
    perf = {
        "name": name,
        "clicks": random.randint(50, 500),
        "sales": random.randint(0, 20),
        "trend": round(random.uniform(0.8, 1.4), 2)
    }
    res = requests.post(
        f"{BACKEND}/api/growth/evaluate",
        headers=HEADERS,
        json=perf
    ).json()
    print("[Growth] Evaluation:", res)
    return res

# -----------------------------------------------------------
# MAIN CYCLE
# -----------------------------------------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (DEBUG)")
    print("--------------------------------------")

    # Generate
    t = generate_template()
    if not t or "name" not in t:
        print("⚠️ Template generation failed")
        return

    name = t["name"]
    zip_path = t.get("zip")

    # Growth Score
    g = growth_score(name)

    # Scaling
    if g.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal Scale")
        scale_template(name)

    # Monetization
    if zip_path:
        print("\n💰 Monetizing...")
        run_all_streams_micro_engine(zip_path, name)


# -----------------------------------------------------------
# Worker Loop
# -----------------------------------------------------------
if __name__ == "__main__":
    print("🚀 JRAVIS WORKER ONLINE — FULL AUTOMATION MODE")

    while True:
        run_cycle()
        time.sleep(3)
