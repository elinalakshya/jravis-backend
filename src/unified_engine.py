# src/unified_engine.py

import os
import traceback

from publishing_engine import run_publishers


def run_all_streams_micro_engine(
    zip_path: str,
    template_name: str,
    backend_url: str,
):
    """
    Unified execution engine.
    Called by JRAVIS worker after ZIP is streamed locally.

    Args:
        zip_path (str): local path to ZIP file
        template_name (str): template name
        backend_url (str): backend base URL
    """

    print("🚀 UNIFIED ENGINE STARTED")
    print(f"📦 ZIP PATH      : {zip_path}")
    print(f"🧩 TEMPLATE NAME : {template_name}")
    print(f"🌐 BACKEND URL   : {backend_url}")

    if not zip_path or not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    title = template_name
    description = template_name

    try:
        print("📤 STARTING PUBLISHING PIPELINE...")
        results = run_publishers(
            title=title,
            description=description,
            zip_path=zip_path,
        )
        print("✅ PUBLISHING COMPLETED")
        print("📊 RESULTS:", results)
        return results

    except Exception as e:
        print("❌ UNIFIED ENGINE FAILED")
        traceback.print_exc()
        raise e

