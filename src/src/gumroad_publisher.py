import requests
import os

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def publish_to_gumroad(title, description, price_rs, file_path):
    print("🔐 TOKEN PRESENT:", bool(GUMROAD_TOKEN))
    if GUMROAD_TOKEN:
        print("🔐 TOKEN PREFIX:", GUMROAD_TOKEN[:6])

    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")

    headers = {
        "Accept": "application/json",
        "User-Agent": "JRAVIS-Bot/1.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # -----------------------------
    # 1. CREATE PRODUCT
    # -----------------------------
    print("🟢 Creating new Gumroad product...")

    create_url = "https://api.gumroad.com/v2/products"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_rs * 100),
        "description": description,
    }

    r = requests.post(create_url, data=data, headers=headers, timeout=60)

    print("🟢 Create status:", r.status_code)
    print("🟢 Create headers:", r.headers.get("content-type"))
    print("🟢 Create response preview:")
    print(r.text[:500])

    if r.status_code not in (200, 201):
        raise Exception("❌ Gumroad create HTTP failed")

    try:
        resp = r.json()
    except Exception:
        raise Exception("❌ Gumroad create not returning JSON (likely auth blocked)")

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
            headers={"Accept": "application/json"},
            timeout=120,
        )

    print("📤 Upload status:", upload.status_code)
    print("📤 Upload response preview:")
    print(upload.text[:300])

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
        headers={"Accept": "application/json"},
        timeout=60,
    )

    print("🚀 Publish status:", p.status_code)
    print("🚀 Publish response preview:")
    print(p.text[:300])

    if p.status_code not in (200, 201):
        raise Exception("❌ Gumroad publish failed")

    print("💰 PRODUCT LIVE:", product_url)
    return product_url

