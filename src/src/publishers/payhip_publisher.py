# src/src/publishers/payhip_publisher.py

import os
import requests


def publish_to_payhip(title: str, description: str, zip_path: str):
    """
    Uploads a ZIP product to Payhip.
    Contract: (title, description, zip_path)
    """
    api_key = os.getenv("PAYHIP_API_KEY")
    if not api_key:
        raise RuntimeError("PAYHIP_API_KEY not set")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(zip_path)

    url = "https://payhip.com/api/v1/products"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(zip_path, "rb") as f:
        files = {"file": f}
        data = {
            "title": title,
            "description": description,
            "price": "5.00",
        }

        r = requests.post(url, headers=headers, data=data, files=files, timeout=60)
        r.raise_for_status()

    return {"platform": "payhip", "status": "success", "title": title}
