from gumroad_publisher import publish_to_gumroad


def run_publishers(title, description, price, zip_path):
    results = {}

    print("💼 RUNNING PUBLISHERS (GUMROAD AUTO MODE)")

    try:
        print("🟠 Publishing to Gumroad...")
        gumroad_url = publish_to_gumroad(
            title=title,
            description=description,
            price=price,
            file_path=zip_path,
        )
        results["gumroad"] = gumroad_url
        print("🟢 Gumroad SUCCESS:", gumroad_url)

    except Exception as e:
        print("❌ Gumroad FAILED:", str(e))
        results["gumroad"] = None

    return results
