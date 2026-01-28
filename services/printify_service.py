import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")

BASE_URL = "https://api.printify.com/v1"


def _headers():
    return {
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    }


def upload_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise Exception(f"Image not found: {image_path}")

    url = f"{BASE_URL}/uploads/images.json"

    with open(image_path, "rb") as f:
        files = {
            "file": ("design.png", f, "image/png"),
        }

        r = requests.post(url, headers=_headers(), files=files)

    if r.status_code != 200:
        raise Exception(f"Printify upload failed {r.status_code}: {r.text}")

    data = r.json()
    return data["id"]


def create_draft_product(payload: dict) -> dict:
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    if not shop_id:
        raise Exception("PRINTIFY_SHOP_ID not set")

    url = f"{BASE_URL}/shops/{shop_id}/products.json"

    r = requests.post(url, headers={**_headers(), "Content-Type": "application/json"}, json=payload)

    if r.status_code not in (200, 201):
        raise Exception(f"Product create failed {r.status_code}: {r.text}")

    return r.json()
