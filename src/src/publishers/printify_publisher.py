# src/src/publishers/printify_publisher.py

import os


def publish_to_printify(title: str, description: str, zip_path: str):
    """
    Placeholder for Printify automation.
    Contract: (title, description, zip_path)
    """
    api_key = os.getenv("PRINTIFY_API_KEY")
    if not api_key:
        raise RuntimeError("PRINTIFY_API_KEY not set")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(zip_path)

    # NOTE: Printify requires product + variant logic.
    # This stub ensures signature alignment without runtime crash.
    return {
        "platform": "printify",
        "status": "queued",
        "title": title,
        "note": "Printify integration stub (safe)"
    }
