import requests
import os

API = "https://api.printify.com/v1"
TOKEN = os.getenv("PRINTIFY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def create_product_draft(shop_id, data):
    payload = {
        "title": data["title"],
        "description": data["description"],
        "blueprint_id": 6,
        "print_provider_id": 99,

        "variants": [
            {
                "id": 1,
                "price": data["price"] * 100,
                "is_enabled": True
            }
        ],

        "print_areas": [
            {
                "variant_ids": [1],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {"id": data["design_image"]}
                        ]
                    }
                ]
            }
        ]
    }

    r = requests.post(
        f"{API}/shops/{shop_id}/products.json",
        headers=HEADERS,
        json=payload
    )

    print(r.text)

    if r.status_code != 201:
        raise Exception(f"Printify product create failed: {r.status_code} {r.text}")

    return r.json()

