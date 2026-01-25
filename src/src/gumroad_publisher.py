# src/src/gumroad_publisher.py

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
        "price": int(price * 100),  # paise
        "description": description,
    }

    r = requests.post(create_url, data=data, timeout=60)

    print("🟢 Create status:", r.status_code)
    print("🟢 Create text:", r.text[:300])

    if r.status_code != 200:
        raise Exception("❌ Gumroad create HTTP failed")

    try:
        resp = r.json()
    except Exception:
        raise Exception("❌ Gumroad create did not return JSON")

    if not resp.get("success"):
        raise Exception(f"❌ Gumroad create failed: {resp}")

    product_id = resp["product"]["id"]
    product_url = resp["product"]["short_url"]

    print("🆔 PRODUCT ID:", product_id)

    # -----------------------
    # 2. UPLOAD FILE
    # -----------------------
    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(file_path, "rb") as f:
        upload = requests.post(
            upload_url,
            data={"access_token": GUMROAD_TOKEN},
            files={"file": f},
            timeout=120,
        )

    print("🟢 Upload status:", upload.status_code)
    print("🟢 Upload text:", upload.text[:300])

    if upload.status_code != 200:
        raise Exception("❌ Gumroad upload HTTP failed")

    try:
        up = upload.json()
    except Exception:
        raise Exception("❌ Gumroad upload did not return JSON")

    if not up.get("success"):
        raise Exception(f"❌ Gumroad upload failed: {up}")

    # -----------------------
    # 3. PUBLISH PRODUCT
    # -----------------------
    publish_url = f"https://api.gumroad.com/v2/products/{product_id}"

    p = requests.put(
        publish_url,
        data={"access_token": GUMROAD_TOKEN, "published": True},
        timeout=60,
    )

    print("🟢 Publish status:", p.status_code)
    print("🟢 Publish text:", p.text[:300])

    if p.status_code != 200:
        raise Exception("❌ Gumroad publish HTTP failed")

    try:
        presp = p.json()
    except Exception:
        raise Exception("❌ Gumroad publish did not return JSON")

    if not presp.get("success"):
        raise Exception(f"❌ Gumroad publish failed: {presp}")

    print("🎉 GUMROAD PUBLISHED:", product_url)
    return product_url
