# -----------------------------------------------------------
# JRAVIS WORKER — DEBUG MODE (BOOT DIAGNOSTICS)
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

print("🔧 JRAVIS WORKER BOOTING...")

# SHOW CURRENT FILE LOCATION
print("📍 Worker Base Path:", os.path.dirname(__file__))

# SHOW DIRECTORY CONTENT
print("\n📂 Listing Current Folder:")
for f in os.listdir("."):
    print(" -", f)

# -----------------------------------------------------------
# FIX PYTHON PATH
# -----------------------------------------------------------
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "src")
print("\n🔧 Adding ENGINE PATH:", ENGINE_PATH)

if ENGINE_PATH not in sys.path:
    sys.path.append(ENGINE_PATH)

print("🔍 sys.path now:")
for p in sys.path:
    print(" -", p)

# -----------------------------------------------------------
# TEST ENGINE IMPORT
# -----------------------------------------------------------
print("\n🧪 Testing unified_engine import...")

try:
    from unified_engine import run_all_streams_micro_engine
    print("✅ SUCCESS: unified_engine imported correctly!")
except Exception as e:
    print("❌ FAILED to import unified_engine:", e)
    raise SystemExit(1)

# -----------------------------------------------------------
# BACKEND
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
print("\n🌐 BACKEND URL:", BACKEND)

# -----------------------------------------------------------
#  START WORKER
# -----------------------------------------------------------
print("\n🚀 JRAVIS WORKER STARTED — DEBUG MODE ON\n")


def generate_template():
    try:
        print("[Factory] Requesting Template...")
        res = requests.post(f"{BACKEND}/api/factory/generate").json()
        print("[Factory] Response:", res)
        return res
    except Exception as e:
        print("❌ Factory Error:", e)
        return None


def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE (DEBUG)")
    print("--------------------------------------")

    tmpl = generate_template()
    if not tmpl:
        print("❌ Template Generation Failed")
        return

    print("⚡ Template Name:", tmpl.get("name"))


while True:
    run_cycle()
    print("💤 Sleeping 3 seconds...\n")
    time.sleep(3)
