from publisher_payhip import publish_to_payhip


def run_publishers(title, description, zip_path):
    print("💼 RUNNING PUBLISHERS (PAYHIP MODE)")

    result = {}

    try:
        print("🟣 Publishing to Payhip...")
        url = publish_to_payhip(
            title=title,
            description=description,
            file_path=zip_path,
            price=199,
        )
        result["payhip"] = url
    except Exception as e:
        print("❌ PAYHIP ERROR:", e)
        result["payhip"] = None

    return result
