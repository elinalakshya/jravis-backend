from publishing_engine import run_publishers


def run_all_streams_micro_engine(title, description, price, zip_path):
    print("🚀 UNIFIED ENGINE STARTED")
    print("📦 FILE PATH :", zip_path)
    print("🧩 TITLE     :", title)
    print("💰 PRICE     :", price)

    print("📤 STARTING PUBLISHING PIPELINE")

    results = run_publishers(
        title=title,
        description=description,
        price=price,
        zip_path=zip_path,
    )

    print("🏁 PUBLISHING FINISHED")
    return results
