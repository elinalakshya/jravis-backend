import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

headers = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}


def run_pod(count=20):

    print("SHOP ID =", PRINTIFY_SHOP_ID)

    for i in range(count):

        title = f"Minimal Motivational Quote #{i+1}"

        product = {
            "title": title,
            "description": "Minimal bold text t-shirt",
            "blueprint_id": 6,
            "print_provider_id": 1,
            "visible": False,
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
            json=product
        )

        if resp.status_code == 201:
            print("✅ Draft created")
        else:
            print("❌ Error:", resp.text)
