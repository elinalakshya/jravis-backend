from gumroad_publisher import publish_to_gumroad


def run_publishers(title, description, price, zip_path):
    print("💼 RUNNING PUBLISHERS (GUMROAD AUTO MODE)")

    result = {}

    try:
        url = publish_to_gumroad(
            title=title,
            description=description,
            price=price,
            file_path=zip_path,
        )
        result["gumroad"] = url
    except Exception as e:
        print("❌ Gumroad FAILED:", e)
        result["gumroad"] = None

    return result

