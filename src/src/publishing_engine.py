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
