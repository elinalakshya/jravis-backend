import os
import base64
import requests

BASE = "https://api.printify.com/v1"

API_KEY = os.getenv("PRINTIFY_API_KEY")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


# -------------------------
# headers
# -------------------------
def _headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


# -------------------------
# image upload (safe)
# -------------------------
def upload_image(path_or_url: str) -> str:
    """
    If URL -> return URL directly (best method)
    If local file -> upload to printify
    """

    if path_or_url.startswith("http"):
        return path_or_url

    with open(path_or_url, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    payload = {
        "file_name": os.path.basename(path_or_url),
        "contents": encoded
    }

    r = requests.post(
        f"{BASE}/uploads/images.json",
        headers=_headers(),
        json=payload
    )

    if r.status_code not in [200, 201]:
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    return r.json()["id"]


# -------------------------
# MAIN FUNCTION (THIS ONE)
# -------------------------
def create_product_draft(shop_id: int, payload: dict):
    """
    Creates Printify draft product
    """

    r = requests.post(
        f"{BASE}/shops/{shop_id}/products.json",
        headers=_headers(),
        json=payload
    )

    if r.status_code not in [200, 201]:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

