import os
import requests

ETSY_TOKEN = os.getenv("ETSY_TOKEN")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID")


def _headers():
    return {
        "Authorization": f"Bearer {ETSY_TOKEN}",
        "Content-Type": "application/json"
    }


def create_draft_listing(title, description, tags, price=5.99, quantity=999):
    url = f"https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings"

    data = {
        "title": title[:140],
        "description": description,
        "price": price,
        "quantity": quantity,
        "who_made": "i_did",
        "when_made": "made_to_order",
        "taxonomy_id": 69150433,
        "tags": tags[:13],
        "state": "draft"
    }

    r = requests.post(url, headers=_headers(), json=data, timeout=60)
    r.raise_for_status()
    return r.json()["listing_id"]


def upload_image(listing_id, image_path):
    url = f"https://openapi.etsy.com/v3/application/listings/{listing_id}/images"
    headers = {"Authorization": f"Bearer {ETSY_TOKEN}"}

    with open(image_path, "rb") as f:
        files = {"image": f}
        r = requests.post(url, headers=headers, files=files, timeout=120)
        r.raise_for_status()
