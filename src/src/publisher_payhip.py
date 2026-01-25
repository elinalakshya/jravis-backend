import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")

BASE_URL = "https://payhip.com/api/v1"


def publish_to_payhip(title, description, price, file_path):
    if not PAYHIP_API_KEY:
        raise Exception("❌ PAYHIP_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}",
        "Accept": "application/json",
    }

    print("🟣 Creating product on Payhip...")

    # -------------------------
    # 1. CREATE PRODUCT
    # -------------------------
    create_url = f"{BASE_URL}/products"

    data = {
        "title": title,
        "description": description,
        "price": int(price),
        "currency": "INR",
    }

    r = requests.post(create_url, json=data, headers=headers, timeout=60)

    print("🟢 Create status:", r.status_code)
    print("🟢 Create response:", r.text[:300])

    if r.status_code not in (200, 201):
        raise Exception("❌ Payhip product creation failed")

    product = r.json()
    product_id = product.get("id")
    product_url = product.get("url")

    if not product_id:
        raise Exception("❌ Payhip product id missing")

    print("✅ PRODUCT CREATED:", product_id)

    # -------------------------
    # 2. UPLOAD FILE
    # -------------------------
    upload_url = f"{BASE_URL}/products/{product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        up = requests.post(upload_url, headers=headers, files=files, timeout=120)

    print("🟢 Upload status:", up.status_code)
    print("🟢 Upload response:", up.text[:300])

    if up.status_code not in (200, 201):
        raise Exception("❌ Payhip file upload failed")

    print("✅ FILE UPLOADED TO PAYHIP")

    return product_url
