# src/src/unified_engine.py

import os
import traceback
from publishing_engine import run_publishers


def run_all_streams_micro_engine(*, title, description, price, zip_path, backend_url="api"):
    print("🚀 UNIFIED ENGINE STARTED")
    print(f"📦 FILE PATH     : {zip_path}")
    print(f"🧩 TITLE         : {title}")
    print(f"💰 PRICE         : {price}")
    print(f"🌐 BACKEND URL   : {backend_url}")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"File not found: {zip_path}")

    try:
        print("📤 STARTING PUBLISHING PIPELINE")

        results = run_publishers(
            title=title,
            description=description,
            price=price,
            zip_path=zip_path,
        )

        print("✅ PUBLISHING COMPLETED")
        print("📊 RESULTS:", results)
        return results

    except Exception:
        print("❌ UNIFIED ENGINE FAILED")
        traceback.print_exc()
        raise
