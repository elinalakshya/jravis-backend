import os
import requests
import base64
from openai import OpenAI

client = OpenAI()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


headers = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}


def run_pod(count=5):

    print("SHOP ID =", PRINTIFY_SHOP_ID)

    for i in range(count):

        prompt = f"Minimal bold motivational t-shirt quote {i+1}"
        print("🎨 Generating:", prompt)

        # 1. generate image
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = img.data[0].b64_json

        # 2. upload image
        upload = requests.post(
            "https://api.printify.com/v1/uploads/images.json",
            headers=headers,
            json={
                "file_name": f"design{i}.png",
                "contents": image_base64
            }
        ).json()

        image_url = upload.get("preview_url")  # IMPORTANT

        if not image_url:
            print("❌ upload failed:", upload)
            continue

        # 3. create draft product
        product = {
            "title": prompt,
            "description": "Created automatically by JRAVIS",
            "blueprint_id": 6,
            "print_provider_id": 1,
            "visible": False,   # ⭐ REQUIRED FOR DRAFT
            "variants": [
                {
                    "id": 40171,
                    "price": 2200,
                    "is_enabled": True
                }
            ],
            "images": [
                {
                    "src": image_url,
                    "position": "front",
                    "is_default": True
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
            print("❌ Product failed:", resp.text)
