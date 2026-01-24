# src/src/publishing_engine.py

from publisher_payhip import publish_to_payhip


def run_publishers(title: str, description: str, zip_path: str):
    print("💼 RUNNING PUBLISHERS (PAYHIP ONLY MODE)")

    results = {}

    try:
        print("🟣 Publishing to Payhip...")
        url = publish_to_payhip(
            title=title,
            description=description,
            file_path=zip_path,
        )
        results["payhip"] = url
        print("✅ PAYHIP DONE:", url)

    except Exception as e:
        print("❌ PAYHIP FAILED:", str(e))
        results["payhip"] = None

    return results

