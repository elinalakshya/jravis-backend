# publisher_payhip.py

import os
import requests


PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")


def publish_to_payhip(title: str, description: str, file_path: str):
    print("🟣 PAYHIP API CALL STARTED")

    if not PAYHIP_API_KEY:
        raise Exception("❌ PAYHIP_API_KEY not set")

    if not os.path.exists(file_path):
        raise Exception(f"❌ File not found: {file_path}")

    url = "https://payhip.com/api/v2/products"

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}"
    }

    data = {
        "title": title,
        "description": description,
        "price": "199",  # INR — you can later make dynamic
        "currency": "INR"
    }

    files = {
        "file": open(file_path, "rb")
    }

    print("🟣 Uploading product to Payhip...")

    r = requests.post(url, headers=headers, data=data, files=files, timeout=120)

    print("🟣 Payhip status:", r.status_code)
    print("🟣 Payhip response:", r.text[:500])

    if r.status_code not in (200, 201):
        raise Exception("❌ Payhip upload failed")

    try:
        resp = r.json()
    except Exception:
        raise Exception("❌ Payhip did not return JSON")

    product_url = resp.get("url") or resp.get("product_url")

    if not product_url:
        print("⚠️ Payhip response JSON:", resp)
        raise Exception("❌ Payhip product URL not found")

    print("🟢 PAYHIP DONE:", product_url)

    return product_url

