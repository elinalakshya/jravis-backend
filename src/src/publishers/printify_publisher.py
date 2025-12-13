# src/src/publishers/gumroad_publisher.py

import os
import requests

def publish_to_gumroad(title, description, zip_path=None):
    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        print("⚠️ Gumroad API key missing, skipping")
        return {"platform": "gumroad", "status": "skipped"}

    if not zip_path or not os.path.isfile(zip_path):
        raise FileNotFoundError(f"Gumroad ZIP not found: {zip_path}")

    url = "https://api.gumroad.com/v2/products"
    files = {"content": open(zip_path, "rb")}
    data = {
        "name": title,
        "description": description,
        "price": 100,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    r = requests.post(url, headers=headers, data=data, files=files)
    r.raise_for_status()

    print("🟢 Gumroad published:", title)
    return r.json()
