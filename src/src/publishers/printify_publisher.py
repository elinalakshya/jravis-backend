# src/src/publishers/printify_publisher.py

def publish_to_printify(title, description, zip_path=None):
    print(f"🖨️ Printify skipped (no zip needed): {title}")
    return {
        "platform": "printify",
        "status": "skipped",
        "title": title,
    }
