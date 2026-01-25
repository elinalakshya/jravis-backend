# jravis-backend/src/src/unified_engine.py

import os
import traceback

from publishing_engine import run_publishers


def run_all_streams_micro_engine(
    zip_path: str,
    template_name: str,
    backend_url: str,
):
    print("🚀 UNIFIED ENGINE STARTED")
    print(f"📦 ZIP PATH      : {zip_path}")
    print(f"🧩 TEMPLATE NAME : {template_name}")
    print(f"🌐 BACKEND URL   : {backend_url}")

    if not zip_path or not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    # -------------------------
    # PRODUCT META (CLEAN)
    # -------------------------
    title = template_name.replace("_", " ").title()
    description = (
        f"Instant digital download: {title}.\n\n"
        f"This product is part of the JRAVIS automated productivity toolkit series. "
        f"Download instantly and start using today."
    )

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
