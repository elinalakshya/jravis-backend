# src/src/publishing_engine.py

import os
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify

def run_publishers(title, description, zip_path):
    print("🚀 run_publishers() ENTERED")
    print("📦 ZIP PATH =", zip_path)

    results = []

    if os.getenv("GUMROAD_API_KEY"):
        print("🟢 Gumroad publishing triggered")
        results.append(publish_to_gumroad(title, description, zip_path))
    else:
        print("🔴 Gumroad skipped (no key)")

    if os.getenv("PAYHIP_API_KEY"):
        print("🟢 Payhip publishing triggered")
        results.append(publish_to_payhip(title, description, zip_path))
    else:
        print("🔴 Payhip skipped (no key)")

    if os.getenv("PRINTIFY_API_KEY"):
        print("🟢 Printify publishing triggered")
        results.append(publish_to_printify(title, description, zip_path))
    else:
        print("🔴 Printify skipped (no key)")

    print("✅ run_publishers() EXIT")
    return results

    # --- Gumroad ---
    if os.getenv("GUMROAD_API_KEY"):
        results.append(
            publish_to_gumroad(title, description, zip_path)
        )

    # --- Payhip ---
    if os.getenv("PAYHIP_API_KEY"):
        results.append(
            publish_to_payhip(title, description, zip_path)
        )

    # --- Printify ---
    if os.getenv("PRINTIFY_API_KEY"):
        results.append(
            publish_to_printify(title, description, zip_path)
        )

    return results
