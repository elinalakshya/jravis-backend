# src/src/publishers/printify_publisher.py

def publish_to_printify(title, description, zip_path=None):
    """
    Printify does not use zip files directly.
    zip_path is accepted for interface compatibility.
    """
    print(f"🖨️ Printify publish skipped (no ZIP upload required): {title}")
    return {
        "platform": "printify",
        "status": "skipped",
        "title": title,
    }
