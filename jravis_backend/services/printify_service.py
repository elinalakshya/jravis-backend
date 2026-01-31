import os
import requests

BASE = "https://api.printify.com/v1"

API_KEY = os.getenv("PRINTIFY_API_KEY")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


# ===============================
# Upload image to Printify
# ===============================
def upload_image(path: str) -> str:
    url = f"{BASE}/uploads/images.json"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    with open(path, "rb") as f:
        files = {
            "file_name": (None, os.path.basename(path)),
            "contents": (os.path.basename(path), f, "image/png"),
        }

        r = requests.post(url, headers=headers, files=files)

    if r.status_code != 200:
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    return r.json()["id"]


# ===============================
# Create product draft
# ===============================
def create_product_draft(shop_id: str, payload: dict):
    url = f"{BASE}/shops/{shop_id}/products.json"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code not in [200, 201]:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

