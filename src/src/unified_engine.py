from publishing_engine import run_publishers


def run_all_streams_micro_engine(product: dict, backend_url="api"):
    try:
        title = product["title"]
        description = product["description"]
        price = product["price"]
        zip_path = product["zip_path"]

        print("🚀 UNIFIED ENGINE STARTED")
        print("📦 ZIP PATH      :", zip_path)
        print("🧩 TEMPLATE NAME :", title)
        print("🌐 BACKEND URL   :", backend_url)
        print("📤 STARTING PUBLISHING PIPELINE")

        results = run_publishers(
            title=title,
            description=description,
            price=price,
            zip_path=zip_path,
        )

        print("🏁 PUBLISHING FINISHED")
        print("📊 RESULTS:", results)

        return results

    except Exception as e:
        print("❌ UNIFIED ENGINE FAILED")
        raise e
