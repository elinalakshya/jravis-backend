print("🚀 JRAVIS POD STARTED")

import os
import base64
import requests
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------
# Load environment variables (.env)
# -------------------------------------------------
load_dotenv()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PRINTIFY_API_KEY or not PRINTIFY_SHOP_ID or not OPENAI_API_KEY:
    raise Exception("❌ Missing keys in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)


# -------------------------------------------------
# Step 1 — Generate AI prompt
# -------------------------------------------------
def ai_generate_design_prompt():
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": "Create a short trendy motivational t-shirt design idea (5-8 words only)"
        }]
    )
    return res.choices[0].message.content.strip()


# -------------------------------------------------
# Step 2 — Generate AI image
# -------------------------------------------------
def generate_image(prompt):
    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return img.data[0].b64_json


# -------------------------------------------------
# Step 3 — Upload to Printify
# -------------------------------------------------
def upload_to_printify(image_base64):
    resp = requests.post(
        "https://api.printify.com/v1/uploads/images.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        json={
            "file_name": "design.png",
            "contents": image_base64
        }
    ).json()

    return resp["url"]


# -------------------------------------------------
# Step 4 — Create product
# -------------------------------------------------
def create_product(image_url, title):
    product_data = {
        "title": f"{title} | JRAVIS POD",
        "description": "Auto-generated design by JRAVIS",
        "blueprint_id": 6,
        "print_provider_id": 1,
        "variants": [
            {"id": 40171, "price": 2200, "is_enabled": True}
        ],
        "images": [
            {"src": image_url, "position": "front", "is_default": True}
        ]
    }

    resp = requests.post(
        f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json",
        headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"},
        json=product_data
    ).json()

    return resp


# -------------------------------------------------
# MAIN RUNNER
# -------------------------------------------------
def run():
    print("⚡ Generating prompt...")
    prompt = ai_generate_design_prompt()
    print("🎨 Prompt:", prompt)

    print("🖼 Generating image...")
    image_b64 = generate_image(prompt)

    print("⬆ Uploading to Printify...")
    image_url = upload_to_printify(image_b64)

    print("🛍 Creating product...")
    product = create_product(image_url, prompt)

    print("✅ SUCCESS PRODUCT CREATED")
    print(product)


# -------------------------------------------------
# ENTRY POINT (IMPORTANT)
# -------------------------------------------------
if __name__ == "__main__":
    run()
