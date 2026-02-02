from openai import OpenAI
import requests, os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


def upload_to_printify(image_b64, idx):
    resp = requests.post(
        "https://api.printify.com/v1/uploads/images.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        json={
            "file_name": f"design{idx}.png",
            "contents": image_b64
        }
    )

    data = resp.json()

    if "preview_url" not in data:
        print("❌ Upload failed:", data)
        return None

    return data["preview_url"]

def run_pod(count=20):
    for i in range(count):
        try:
            prompt = f"Minimal bold motivational t-shirt quote {i+1}"
            print("🎨 Generating:", prompt)

            img = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )

            image_b64 = img.data[0].b64_json

            image_url = upload_to_printify(image_b64, i)

            if not image_url:
                continue

            product = {
                "title": prompt,
                "description": "JRAVIS Auto Draft",
                "blueprint_id": 6,
                "print_provider_id": 1,
                "is_published": False,
                "variants": [{"id": 40171, "price": 2200, "is_enabled": True}],
                "images": [{"src": image_url, "position": "front"}]
            }

            requests.post(
                f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
                headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
                json=product
            )

            print("✅ Draft created")

        except Exception as e:
            print("❌ POD job error:", e)
