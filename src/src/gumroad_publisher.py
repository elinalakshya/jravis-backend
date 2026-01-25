import os
import requests

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def publish_to_gumroad(title, description, price, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("❌ GUMROAD_TOKEN not set")

    print("🟢 Creating Gumroad product...")

    # STEP 1 — Create product (no file)
    create_url = "https://api.gumroad.com/v2/products"
    create_data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "description": description,
        "price": int(price) * 100,  # in paise
    }

    r = requests.post(create_url, data=create_data, timeout=60)

    if r.status_code != 200:
        print("Create response:", r.text)
        raise Exception("❌ Gumroad create HTTP failed")

    resp = r.json()

    if not resp.get("success"):
        raise Exception(f"❌ Gumroad create failed: {resp}")

    product_id = resp["product"]["id"]
    print("✅ Product created:", product_id)

    # STEP 2 — Upload file
    print("📤 Uploading file to Gumroad product...")

    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"access_token": GUMROAD_TOKEN}
        up = requests.post(upload_url, data=data, files=files, timeout=120)

    if up.status_code != 200:
        print("Upload response:", up.text)
        raise Exception("❌ Gumroad upload HTTP failed")

    upj = up.json()
    if not upj.get("success"):
        raise Exception(f"❌ Gumroad upload failed: {upj}")

    print("✅ File uploaded")

    # STEP 3 — Publish product
    print("🚀 Publishing product...")

    pub_url = f"https://api.gumroad.com/v2/products/{product_id}"
    pub_data = {
        "access_token": GUMROAD_TOKEN,
        "published": True
    }

    pr = requests.put(pub_url, data=pub_data, timeout=60)

    if pr.status_code != 200:
        print("Publish response:", pr.text)
        raise Exception("❌ Gumroad publish HTTP failed")

    prj = pr.json()
    if not prj.get("success"):
        raise Exception(f"❌ Gumroad publish failed: {prj}")

    product_url = prj["product"]["short_url"]
    print("🎉 LIVE GUMROAD LINK:", product_url)

    return product_url

