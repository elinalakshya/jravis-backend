import os
import requests


GUMROAD_CREATE_URL = "https://api.gumroad.com/v2/products"


def publish_to_gumroad(title, description, price, file_path):
    token = os.getenv("GUMROAD_TOKEN")

    if not token:
        raise Exception("❌ GUMROAD_TOKEN not set")

    print("🔐 TOKEN PRESENT: True")

    data = {
        "access_token": token,
        "product[name]": title,
        "product[description]": description,
        "product[price]": int(price) * 100,  # paise
    }

    files = {
        "product[file]": open(file_path, "rb")
    }

    print("🟢 Creating Gumroad product...")

    r = requests.post(
        GUMROAD_CREATE_URL,
        data=data,
        files=files,
        timeout=60
    )

    print("🟢 HTTP STATUS:", r.status_code)
    print("🟢 RAW RESPONSE:", r.text[:300])

    if r.status_code != 200:
        raise Exception("❌ Gumroad create HTTP failed")

    try:
        resp = r.json()
    except Exception:
        raise Exception("❌ Gumroad did not return JSON")

    if not resp.get("success"):
        raise Exception(f"❌ Gumroad create failed: {resp}")

    product = resp["product"]
    return product.get("short_url")
