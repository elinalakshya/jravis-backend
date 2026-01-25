from publisher_payhip import publish_to_payhip


def run_publishers(title, description, zip_path):
    print("💼 RUNNING PUBLISHERS (PAYHIP ONLY MODE)")

    results = {}

    try:
        print("🟣 Publishing to Payhip...")
        payhip_url = publish_to_payhip(
            title=title,
            description=description,
            file_path=zip_path,
        )
        results["payhip"] = payhip_url
    except Exception as e:
        print("❌ PAYHIP FAILED:", e)
        results["payhip"] = None

    print("🏁 PUBLISHING FINISHED")
    return results

