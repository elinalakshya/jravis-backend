
import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")

BASE = "https://api.printify.com/v1"

HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}


def upload_image(image_path: str) -> str:

    if not PRINTIFY_API_KEY:
        raise Exception("PRINTIFY_API_KEY not set")

    files = {
        "file": open(image_path, "rb")
    }

    r = requests.post(
        f"{BASE}/uploads/images.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        files=files
    )

    r.raise_for_status()

    return r.json()["id"]


def create_product(title, description, blueprint_id, provider_id, image_id, variants, price):

    shop_id = get_shop_id()

    payload = {
        "title": title,
        "description": description,
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,
        "variants": variants,
        "print_areas": [
            {
                "variant_ids": [v["id"] for v in variants],
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
        f"{BASE}/shops/{shop_id}/products.json",
        headers=HEADERS,
        json=payload
    )

    r.raise_for_status()

    return r.json()["id"]


def get_shop_id():

    r = requests.get(
        f"{BASE}/shops.json",
        headers=HEADERS
    )

    r.raise_for_status()

    return r.json()[0]["id"]
