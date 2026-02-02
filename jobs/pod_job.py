from openai import OpenAI
import requests, os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

def run_pod(count=20):
    for i in range(count):
        prompt = f"Minimal bold motivational t-shirt quote {i+1}"
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        image_b64 = img.data[0].b64_json

        upload = requests.post(
            "https://api.printify.com/v1/uploads/images.json",
            headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
            json={"file_name": f"design{i}.png", "contents": image_b64}
        ).json()

        product = {
            "title": f"{prompt}",
            "description": "JRAVIS Auto Draft",
            "blueprint_id": 6,
            "print_provider_id": 1,
            "is_published": False,
            "variants": [{"id": 40171, "price": 2200, "is_enabled": True}],
            "images": [{"src": upload["url"], "position": "front"}]
        }

        requests.post(
            f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
            headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
            json=product
        )
