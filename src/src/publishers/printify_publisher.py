import os

def publish_to_printify(title: str, description: str, zip_path: str):
    api_key = os.getenv("PRINTIFY_API_KEY")
    if not api_key:
        raise RuntimeError("PRINTIFY_API_KEY not set")

    # stub for now (safe no-op)
    return {
        "platform": "printify",
        "status": "skipped",
        "title": title
    }
