import os
import requests

BASE = "https://api.printify.com/v1"
TOKEN = os.getenv("PRINTIFY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}


# ==============================
# Upload image to Printify
# ==============================
def upload_image(image_path: str):
    url = f"{BASE}/uploads/images.json"

    with open(image_path, "rb") as f:
        files = {
            "file_name": (os.path.basename(image_path)),
            "contents": f
        }

        r = requests.post(url, headers=HEADERS, files=files)

    if not r.ok:
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    return r.json()["id"]


# ==============================
# Create product draft
# ==============================
def create_product_draft(shop_id: int, payload: dict):
    url = f"{BASE}/shops/{shop_id}/products.json"

    r = requests.post(url, headers={**HEADERS, "Content-Type": "application/json"}, json=payload)

    if not r.ok:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

