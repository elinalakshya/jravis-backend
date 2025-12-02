import requests
import base64
from settings import PRINTIFY_API_KEY, OPENAI_API_KEY
import openai
import os

openai.api_key = OPENAI_API_KEY

PRINTIFY_SHOP_ID = "YOUR_SHOP_ID"  # Fill using your Printify shop ID

def ai_generate_design_prompt():
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Generate a high-quality POD design concept in 10 words"}]
    )
    return response.choices[0].message.content


def publish_printify_product():
    prompt = ai_generate_design_prompt()
    print("🎨 Printify Prompt:", prompt)

    # 1. Generate an AI image
    img = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = img.data[0].b64_json

    # 2. Upload image to Printify
    img_upload = requests.post(
        "https://api.printify.com/v1/uploads/images.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        json={"file_name": "design.png", "contents": image_base64}
    ).json()

    image_url = img_upload.get("url")
    print("🖼 Uploaded Image:", image_url)

    # 3. Create POD product
    product_data = {
        "title": f"Auto Design – {prompt}",
        "description": "Created by JRAVIS Automation",
        "blueprint_id": 6,  # Unisex T-shirt
        "print_provider_id": 1,
        "variants": [{"id": 40171, "price": 2200, "is_enabled": True}],
        "images": [{"src": image_url, "position": "front", "is_default": True}]
    }

    product_resp = requests.post(
        f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        json=product_data
    ).json()

    print("🛍 Product Published:", product_resp)

    return product_resp
