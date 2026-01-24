import requests
import os

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def publish_to_gumroad(title, description, price_rs, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")

    # -----------------------------
    # 1. CREATE PRODUCT
    # -----------------------------
    print("🟢 Creating new Gumroad product...")

    create_url = "https://api.gumroad.com/v2/products"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_rs * 100),  # INR → paise
        "description": description,
    }

    r = requests.post(create_url, data=data, timeout=60)

    print("🟢 Create status:", r.status_code)
    print("🟢 Create response:", r.text[:300])

    try:
        resp = r.json()
    except Exception:
        raise Exception("❌ Gumroad create did not return JSON")

    if not resp.get("success"):
        raise Exception(f"❌ Gumroad create failed: {resp}")

    product_id = resp["product"]["id"]
    product_url = resp["product"]["short_url"]

    print("✅ Product created:", product_id)

    # -----------------------------
    # 2. UPLOAD FILE
    # -----------------------------
    print("📤 Uploading file to Gumroad...")

    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(file_path, "rb") as f:
        upload = requests.post(
            upload_url,
            data={"access_token": GUMROAD_TOKEN},
            files={"file": f},
            timeout=120,
        )

    print("📤 Upload status:", upload.status_code)
    print("📤 Upload response:", upload.text[:300])

    if upload.status_code not in (200, 201):
        raise Exception("❌ Gumroad upload failed")

    # -----------------------------
    # 3. PUBLISH PRODUCT
    # -----------------------------
    print("🚀 Publishing product...")

    publish_url = f"https://api.gumroad.com/v2/products/{product_id}"

    p = requests.put(
        publish_url,
        data={
            "access_token": GUMROAD_TOKEN,
            "published": True,
        },
        timeout=60,
    )

    print("🚀 Publish status:", p.status_code)
    print("🚀 Publish response:", p.text[:300])

    if p.status_code not in (200, 201):
        raise Exception("❌ Gumroad publish failed")

    print("💰 PRODUCT LIVE:", product_url)
    return product_url

