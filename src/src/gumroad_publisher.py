import requests
import os

GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


def publish_to_gumroad(title, description, price_rs, file_path):
    if not GUMROAD_TOKEN:
        raise Exception("GUMROAD_TOKEN not set in environment")

    print("🟠 Creating Gumroad product...")

    create_url = "https://api.gumroad.com/v2/products"

    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "price": int(price_rs * 100),  # paise
        "description": description,
    }

    r = requests.post(create_url, data=data, timeout=60)

    print("🟠 Gumroad create status:", r.status_code)
    print("🟠 Gumroad create response:", r.text[:500])

    try:
        resp = r.json()
    except Exception:
        raise Exception("Gumroad did not return JSON. Check token and response above.")

    if not resp.get("success"):
        raise Exception(f"Gumroad create failed: {resp}")

    product_id = resp["product"]["id"]
    short_url = resp["product"]["short_url"]

    print("📤 Uploading file to Gumroad...")

    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(file_path, "rb") as f:
        upload = requests.post(
            upload_url,
            data={"access_token": GUMROAD_TOKEN},
            files={"file": f},
            timeout=120,
        )

    print("📤 Gumroad upload status:", upload.status_code)
    print("📤 Gumroad upload response:", upload.text[:500])

    try:
        up = upload.json()
    except Exception:
        raise Exception("Gumroad upload did not return JSON")

    if not up.get("success"):
        raise Exception(f"Gumroad upload failed: {up}")

    print("🚀 Gumroad product LIVE:", short_url)
    return short_url

