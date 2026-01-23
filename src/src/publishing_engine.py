# src/src/publishing_engine.py

import traceback
from gumroad_publisher import publish_to_gumroad


def run_publishers(title: str, description: str, zip_path: str):
    print("💼 RUNNING PUBLISHERS (GUMROAD ONLY MODE)")

    results = {}

    try:
        print("🟠 Publishing to Gumroad...")
        gumroad_url = publish_to_gumroad(
            title=title,
            description=description,
            price_rs=199,
            file_path=zip_path,
        )
        results["gumroad"] = gumroad_url
        print("✅ Gumroad SUCCESS:", gumroad_url)

    except Exception as e:
        print("❌ Gumroad FAILED:", e)
        traceback.print_exc()
        results["gumroad"] = None

    print("🏁 PUBLISHING FINISHED")
    return results

