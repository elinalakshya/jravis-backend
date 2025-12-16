import os
from src.publishers.gumroad_publisher import publish_to_gumroad
from src.publishers.payhip_publisher import publish_to_payhip
from src.publishers.printify_publisher import publish_to_printify

def run_publishers(title: str, description: str, zip_path: str):
    results = []

    print("💰 Publishing Engine Triggered")

    if os.getenv("GUMROAD_API_KEY"):
        print("➡️ Publishing to Gumroad")
        results.append(publish_to_gumroad(title, description, zip_path))

    if os.getenv("PAYHIP_API_KEY"):
        print("➡️ Publishing to Payhip")
        results.append(publish_to_payhip(title, description, zip_path))

    if os.getenv("PRINTIFY_API_KEY"):
        print("➡️ Publishing to Printify")
        results.append(publish_to_printify(title, description, zip_path))

    if not results:
        print("⚠️ No API keys found — publishing skipped")

    return results
