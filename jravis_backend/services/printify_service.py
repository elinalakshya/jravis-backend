import os
import requests

BASE = "https://api.printify.com/v1"
TOKEN = os.getenv("PRINTIFY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def create_product_draft(shop_id: int, payload: dict):
    url = f"{BASE}/shops/{shop_id}/products.json"

    r = requests.post(url, headers=HEADERS, json=payload)

    if not r.ok:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

