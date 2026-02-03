import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

headers = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

# ⭐ Stable placeholder image (always works, prevents locking)
PLACEHOLDER_IMAGE = "https://dummyimage.com/1200x1200/ffffff/000000.png&text=Design"


def run_pod(count=20):
    print("🚀 POD factory started")
    print("SHOP ID =", PRINTIFY_SHOP_ID)

    for i in range(count):

        title = f"Minimal Motivational Quote #{i+1}"

        product_payload = {
            "title": title,
            "description": "Clean minimal typography t-shirt design",
            "blueprint_id": 6,          # Unisex T-shirt
            "print_provider_id": 1,

            # ⭐ VERY IMPORTANT → makes it Draft
            "visible": False,

            # ⭐ REQUIRED → prevents locking
            "images": [
                {
                    "src": PLACEHOLDER_IMAGE,
                    "position": "front",
                    "is_default": True
                }
            ],

            # ⭐ Required variant
            "variants": [
                {
                    "id": 40171,
                    "price": 2200,
                    "is_enabled": True
                }
            ]
        }

        resp = requests.post(
            f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json",
            headers=headers,
            json=product_payload
        )

        if resp.status_code == 201:
            print("✅ Draft created:", title)
        else:
            print("❌ Failed:", resp.text)

    print("✅ POD factory finished")
