def run_publishers(file_path, title, description, price):
    print("📤 STARTING PUBLISHING PIPELINE (DRAFT MODE)")
    print("📦 FILE:", file_path)
    print("🧩 TITLE:", title)
    print("💰 PRICE:", price)

    # Draft-only: no auto publishing
    return {
        "status": "draft_only",
        "download_path": file_path
    }
