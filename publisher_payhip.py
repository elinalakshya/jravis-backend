import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")

BASE_URL = "https://payhip.com/api/v2"


def publish_to_payhip(title, description, file_path, price=199):
    print("🟣 PAYHIP PUBLISHER STARTED")

    if not PAYHIP_API_KEY:
        print("❌ PAYHIP_API_KEY not set")
        return None

    print("🔐 PAYHIP KEY PREFIX:", PAYHIP_API_KEY[:5])

    # ---------------------------
    # 1. CREATE PRODUCT
    # ---------------------------
    url = f"{BASE_URL}/products"

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}",
    }

    data = {
        "title": title,
        "description": description,
        "price": price,
        "currency": "INR",
    }

    r = requests.post(url, headers=headers, data=data)

    print("🟣 CREATE STATUS:", r.status_code)
    print("🟣 CREATE RESPONSE:", r.text[:300])

    if r.status_code not in [200, 201]:
        print("❌ Payhip create failed")
        return None

    product = r.json()
    product_id = product.get("id")

    if not product_id:
        print("❌ No product ID from Payhip")
        return None

    print("✅ PAYHIP PRODUCT ID:", product_id)

    # ---------------------------
    # 2. UPLOAD FILE
    # ---------------------------
    upload_url = f"{BASE_URL}/products/{product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        ur = requests.post(upload_url, headers=headers, files=files)

    print("🟣 UPLOAD STATUS:", ur.status_code)
    print("🟣 UPLOAD RESPONSE:", ur.text[:300])

    if ur.status_code not in [200, 201]:
        print("❌ Payhip file upload failed")
        return None

    print("🎉 PAYHIP PUBLISHED SUCCESSFULLY")

    return product.get("permalink") or product.get("url")

