import os
import requests

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def publish_to_gumroad(title, description, price, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")

    print("🔐 TOKEN PREFIX:", GUMROAD_TOKEN[:6])

    # -----------------------
    # 1. CREATE PRODUCT
    # -----------------------
    create_url = "https://api.gumroad.com/v2/products"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price),          # Gumroad expects major currency, not paise
        "description": description,
        "published": "true",
    }

    r = requests.post(create_url, data=data, timeout=60)

    print("🟢 Create status:", r.status_code)
    print("🟢 Create text:", r.text[:300])

    if r.status_code != 200:
        raise Exception("❌ Gumroad create HTTP failed")

    resp = r.json()
    if not resp.get("success"):
        raise Exception(f"❌ Gumroad create failed: {resp}")

    product_id = resp["product"]["id"]
    product_url = resp["product"]["short_url"]

    print("✅ PRODUCT CREATED:", product_id)

    # -----------------------
    # 2. UPLOAD FILE
    # -----------------------
    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"access_token": GUMROAD_TOKEN}
        up = requests.post(upload_url, data=data, files=files, timeout=120)

    print("🟢 Upload status:", up.status_code)
    print("🟢 Upload text:", up.text[:300])

    if up.status_code != 200:
        raise Exception("❌ Gumroad file upload failed")

    upj = up.json()
    if not upj.get("success"):
        raise Exception(f"❌ Gumroad upload failed: {upj}")

    print("✅ FILE ATTACHED TO PRODUCT")

    return product_url

