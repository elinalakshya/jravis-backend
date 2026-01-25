# src/src/publishing_engine.py

from gumroad_publisher import publish_to_gumroad


def run_publishers(title, description, price, zip_path):
    print("💼 RUNNING PUBLISHERS (GUMROAD MODE)")

    results = {}

    try:
        print("🟠 Publishing to Gumroad...")
        url = publish_to_gumroad(
            title=title,
            description=description,   # ✅ FIXED
            price=price,
            file_path=zip_path,
        )
        results["gumroad"] = url

    except Exception as e:
        print("❌ Gumroad FAILED:", e)
        results["gumroad"] = None

    print("🏁 PUBLISHING FINISHED")
    return results


from publisher_payhip import publish_to_payhip

def run_publishers(title, description, price, zip_path):
    results = {}

    print("💼 RUNNING PUBLISHERS (PAYHIP AUTO MODE)")
    try:
        print("🟣 Publishing to Payhip...")
        payhip_url = publish_to_payhip(
            title=title,
            description=description,
            price=price,
            file_path=zip_path,
        )
        results["payhip"] = payhip_url
        print("✅ Payhip DONE:", payhip_url)
    except Exception as e:
        print("❌ Payhip FAILED:", e)
        results["payhip"] = None

    return results
