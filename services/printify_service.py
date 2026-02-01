import os
import requests

PRINTIFY_TOKEN = os.getenv("PRINTIFY_TOKEN")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

BASE = "https://api.printify.com/v1"

HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_TOKEN}",
    "Content-Type": "application/json"
}


# =========================================================
# Upload image to Printify
# =========================================================
def upload_image(file_name: str, image_url: str) -> str:
    """
    Upload external image URL to Printify
    returns image_id
    """

    url = f"{BASE}/uploads/images.json"

    payload = {
        "file_name": file_name,
        "url": image_url
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    r.raise_for_status()

    data = r.json()
    return data["id"]


# =========================================================
# Create POD product (T-shirt blueprint 6 provider 99)
# =========================================================
def create_pod_product(
    title: str,
    description: str,
    price: int,
    design_image_id: str
) -> str:
    """
    Creates product in Printify shop
    returns product_id
    """

    # 🔥 Boss: we use ONLY white S–3XL (fast + stable)
    variant_ids = [
        12102,  # S
        12101,  # M
        12100,  # L
        12103,  # XL
        12104,  # 2XL
        12105   # 3XL
    ]

    url = f"{BASE}/shops/{PRINTIFY_SHOP_ID}/products.json"

    payload = {
        "title": title,
        "description": description,
        "blueprint_id": 6,
        "print_provider_id": 99,

        "variants": [
            {
                "id": vid,
                "price": price,
                "is_enabled": True
            }
            for vid in variant_ids
        ],

        "print_areas": [
            {
                "variant_ids": variant_ids,
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": design_image_id,
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

    r = requests.post(url, headers=HEADERS, json=payload)

    if not r.ok:
        raise Exception(f"Printify create failed: {r.text}")

    data = r.json()
    return data["id"]


# =========================================================
# Publish product (make visible in store)
# =========================================================
def publish_product(product_id: str):
    url = f"{BASE}/shops/{PRINTIFY_SHOP_ID}/products/{product_id}/publish.json"

    r = requests.post(url, headers=HEADERS, json={})
    r.raise_for_status()

    return True

