def publish_to_printify(title, description, zip_path):
    """
    Printify does not use zip_path yet,
    but we accept it to keep interface consistent.
    """
    # TODO: use zip_path later if needed
    print(f"🖨️ Printify publish skipped (no implementation yet): {title}")
    return {"platform": "printify", "status": "skipped"}

