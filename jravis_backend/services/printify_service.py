import os
import base64
import requests

BASE = "https://api.printify.com/v1"
TOKEN = os.getenv("PRINTIFY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


# =================================
# Upload image (BASE64 REQUIRED)
# =================================
def upload_image(image_path: str):
    url = f"{BASE}/uploads/images.json"

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    payload = {
        "file_name": os.path.basename(image_path),
        "contents": encoded
    }

    r = requests.post(url, headers=HEADERS, json=payload)

    if not r.ok:
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    return r.json()["id"]


# =================================
# Create product draft
# =================================
def create_product_draft(shop_id: int, payload: dict):
    url = f"{BASE}/shops/{shop_id}/products.json"

    r = requests.post(url, headers=HEADERS, json=payload)

    if not r.ok:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

