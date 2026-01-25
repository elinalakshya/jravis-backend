# worker.py
import time
import os

from unified_engine import run_all_streams_micro_engine
from product_factory import generate_product

print("🚀 WORKER ONLINE")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "factory_output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

while True:
    try:
        print("\n🔥 RUNNING CYCLE")

        # ----------------------------
        # 1. GENERATE PRODUCT
        # ----------------------------
        product = generate_product()

        if not product or "file_path" not in product:
            print("❌ Factory returned invalid product:", product)
            time.sleep(60)
            continue

        print("📦 PRODUCT READY:", product["file_path"], product["title"])

        # ----------------------------
        # 2. PUBLISH
        # ----------------------------
        print("🚀 CALLING UNIFIED ENGINE")

        results = run_all_streams_micro_engine(
            zip_path=product["file_path"],
            template_name=product["title"],
            backend_url="local",
        )

        print("🟢 PUBLISH RESULT:", results)

    except Exception as e:
        print("❌ WORKER ERROR:", e)

    print("⏳ Sleeping 10 minutes...\n")
    time.sleep(600)

