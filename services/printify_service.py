import os
import requests

PRINTIFY_TOKEN = os.getenv("PRINTIFY_TOKEN")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


def _headers():
    return {
        "Authorization": f"Bearer {PRINTIFY_TOKEN}",
        "Content-Type": "application/json"
    }


# 1. Upload image to Printify
def upload_image(image_path):
    url = "https://api.printify.com/v1/uploads/images.json"

    with open(image_path, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {PRINTIFY_TOKEN}"}
        r = requests.post(url, headers=headers, files=files, timeout=120)
        r.raise_for_status()
        return r.json()["id"]


# 2. Create product (DRAFT)
def create_product(title, description, blueprint_id, provider_id, image_id, variants, price):

    url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json"

    data = {
        "title": title,
        "description": description,
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,
        "variants": [
            {
                "id": v,
                "price": price * 100,
                "is_enabled": True
            } for v in variants
        ],
        "print_areas": [
            {
                "variant_ids": variants,
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1,
                                "angle": 0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    r = requests.post(url, headers=_headers(), json=data, timeout=120)
    r.raise_for_status()
    return r.json()["id"]
