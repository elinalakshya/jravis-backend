def run_all_streams_micro_engine(product):
    print("🚀 UNIFIED ENGINE STARTED")
    print("📦 ZIP PATH :", product["zip_path"])
    print("🧩 TITLE    :", product["title"])
    print("💰 PRICE    :", product["price"])

    return {
        "download_zip": product["zip_path"]
    }
