import os
import traceback

from src.publishing_engine import run_publishers


def run_all_streams_micro_engine(zip_path: str, title: str, backend: str):
    """
    Main unified execution engine.
    - Receives ZIP path
    - Executes publishing pipelines
    """

    print("🚀 UNIFIED ENGINE STARTED")
    print(f"📦 ZIP      : {zip_path}")
    print(f"📝 TITLE    : {title}")
    print(f"🌐 BACKEND  : {backend}")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    try:
        print("📤 Publishing started...")
        results = run_publishers(
            title=title,
            description=title,
            zip_path=zip_path
        )
        print("✅ Publishing completed:", results)
        return results

    except Exception as e:
        print("❌ PUBLISHING FAILED")
        traceback.print_exc()
        raise e

