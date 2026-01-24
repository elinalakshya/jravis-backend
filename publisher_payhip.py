import requests
import os

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")


def publish_to_payhip(title, description, price_rs, file_path):
    if not PAYHIP_API_KEY:
        raise Exception("❌ PAYHIP_API_KEY not set")

    print("🟣 Creating Payhip product...")

    url = "https://payhip.com/api/v2/products"

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}",
    }

    files = {
        "file": open(file_path, "rb"),
    }

    data = {
        "title": title,
        "description": description,
        "price": price_rs,
        "currency": "INR",
    }

    r = requests.post(url, headers=headers, data=data, files=files, timeout=120)

    print("🟣 Status:", r.status_code)
    print("🟣 Response:", r.text[:400])

    if r.status_code not in (200, 201):
        raise Exception("❌ Payhip product creation failed")

    resp = r.json()

    product_url = resp.get("product", {}).get("url") or resp.get("url")

    print("💰 PAYHIP PRODUCT LIVE:", product_url)
    return product_url

