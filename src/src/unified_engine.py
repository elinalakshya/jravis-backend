from publishing_engine import run_publishers
import os
import traceback

def run_all_streams_micro_engine(file_path: str, title: str, price: int):
    print("🚀 UNIFIED ENGINE STARTED")
    print(f"📦 FILE PATH : {file_path}")
    print(f"🧩 TITLE     : {title}")
    print(f"💰 PRICE     : {price}")

    if not file_path or not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        print("📤 STARTING PUBLISHING PIPELINE")

        results = run_publishers(
            title=title,
            price=price,
            file_path=file_path
        )

        print("✅ PUBLISHING COMPLETED")
        print("📊 RESULTS:", results)
        return results

    except Exception:
        print("❌ UNIFIED ENGINE FAILED")
        traceback.print_exc()
        raise
