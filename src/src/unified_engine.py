from publishing_engine import run_publishers


def run_all_streams_micro_engine(file_path, title, description, price):
    print("🚀 UNIFIED ENGINE STARTED")
    print("📦 FILE PATH :", file_path)
    print("🧩 TITLE     :", title)
    print("💰 PRICE     :", price)

    print("📤 STARTING PUBLISHING PIPELINE")
    results = run_publishers(
        file_path=file_path,
        title=title,
        description=description,
        price=price,
    )

    print("✅ PUBLISHING COMPLETED")
    print("📊 RESULTS:", results)

    return results
