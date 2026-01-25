from gumroad_publisher import publish_to_gumroad

def run_publishers(title: str, price: int, file_path: str):
    print("💼 RUNNING PUBLISHERS (GUMROAD MODE)")

    results = {}

    try:
        print("🟠 Publishing to Gumroad...")
        url = publish_to_gumroad(
            title=title,
            price=price,
            file_path=file_path
        )
        results["gumroad"] = url
    except Exception as e:
        print("❌ Gumroad FAILED:", e)
        results["gumroad"] = None

    return results
