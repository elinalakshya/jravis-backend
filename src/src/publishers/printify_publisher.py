# src/src/publishers/printify_publisher.py

def publish_to_printify(title: str, description: str, zip_path: str):
    """
    Upload product to Printify
    """
    # your printify logic here
    return {
        "platform": "printify",
        "status": "success",
        "title": title
    }
