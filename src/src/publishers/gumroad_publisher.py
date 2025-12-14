import os
import requests

def publish_to_gumroad(title: str, description: str, zip_path: str):
    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        raise RuntimeError("GUMROAD_API_KEY not set")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    url = "https://api.gumroad.com/v2/products"
    headers = {"Authorization": f"Bearer {api_key}"}

    data = {
        "name": title,
        "description": description,
        "price": "500",
    }

    with open(zip_path, "rb") as f:
        files = {"content": f}
        r = requests.post(url, data=data, files=files, headers=headers, timeout=60)

    if r.status_code not in (200, 201):
        raise RuntimeError(f"Gumroad failed [{r.status_code}]: {r.text}")

    return r.json()
