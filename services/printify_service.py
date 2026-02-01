import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

BASE = "https://api.printify.com/v1"


def create_product(title, description, price, image_id):

    headers = {
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    blueprint_id = 6
    provider_id = 99

    # ✅ EXACT SAME IDS USED EVERYWHERE
    variant_ids = [
        12126,  # S
        12125,  # M
        12124,  # L
        12127,  # XL
        12128,  # 2XL
        12129   # 3XL
    ]

    variants = [
        {
            "id": v,
            "price": price * 100,
            "is_enabled": True
        }
        for v in variant_ids
    ]

    payload = {
        "title": title,
        "description": description,
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,

        # ✅ must match
        "variants": variants,

        "print_areas": [
            {
                "variant_ids": variant_ids,  # SAME LIST
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

    r = requests.post(
        f"{BASE}/shops/{PRINTIFY_SHOP_ID}/products.json",
        headers=headers,
        json=payload
    )

    if not r.ok:
        raise Exception(f"Printify create failed: {r.text}")

    return r.json()

