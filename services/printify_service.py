import os
import requests

PRINTIFY_TOKEN = os.getenv("PRINTIFY_TOKEN")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


def _headers():
    return {
        "Authorization": f"Bearer {PRINTIFY_TOKEN}",
        "Content-Type": "application/json"
    }


def create_product(title, blueprint_id=122, print_provider_id=1):
    url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json"

    data = {
        "title": title,
        "description": title,
        "blueprint_id": blueprint_id,
        "print_provider_id": print_provider_id,
        "variants": [],
        "print_areas": []
    }

    r = requests.post(url, headers=_headers(), json=data, timeout=60)
    r.raise_for_status()
    return r.json()["id"]
