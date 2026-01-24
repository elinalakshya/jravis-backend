from publisher_payhip import publish_to_payhip


def run_publishers(title, description, zip_path):
    print("💼 RUNNING PUBLISHERS (PAYHIP MODE)")

    results = {}

    try:
        print("🟣 Publishing to Payhip...")
        url = publish_to_payhip(
            title=title,
            description=description,
            price_rs=149,
            file_path=zip_path,
        )
        results["payhip"] = url
    except Exception as e:
        print("❌ Payhip FAILED:", e)
        results["payhip"] = None

    return results
