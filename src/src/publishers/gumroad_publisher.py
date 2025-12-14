# src/src/publishers/gumroad_publisher.py

import os
import requests


def publish_to_gumroad(title: str, description: str, zip_path: str):
    """
    Uploads a ZIP product to Gumroad.
    Contract: (title, description, zip_path)
    """
    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        raise RuntimeError("GUMROAD_API_KEY not set")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(zip_path)

    url = "https://api.gumroad.com/v2/products"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(zip_path, "rb") as f:
        files = {"content": f}
        data = {
            "name": title,
            "description": description,
            "price": "500",  # cents (adjust later)
        }

        r = requests.post(url, headers=headers, data=data, files=files, timeout=60)
        r.raise_for_status()

    return {"platform": "gumroad", "status": "success", "title": title}
