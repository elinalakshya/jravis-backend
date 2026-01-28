import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")


def _headers():
    if not PRINTIFY_API_KEY:
        raise Exception("PRINTIFY_API_KEY not set in environment")
    return {
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    }


# -------------------------------
# Upload image to Printify
# -------------------------------
def upload_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise Exception(f"Design image not found: {image_path}")

    url = "https://api.printify.com/v1/uploads/images.json"

    with open(image_path, "rb") as f:
        files = {
            "file": f,
        }

        r = requests.post(
            url,
            headers=_headers(),
            files=files,
            timeout=60,
        )

    if r.status_code not in (200, 201):
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    data = r.json()
    return data["id"]


# -------------------------------
# Create product draft
# -------------------------------
def create_product_draft(shop_id: str, payload: dict) -> dict:
    url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"

    r = requests.post(
        url,
        headers={**_headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )

    if r.status_code not in (200, 201):
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

