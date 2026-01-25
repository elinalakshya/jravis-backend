import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")

BASE_URL = "https://payhip.com/api/v2/products"


def publish_to_payhip(title, description, file_path, price=199):
    print("🟣 PAYHIP PUBLISHER STARTED")

    if not PAYHIP_API_KEY:
        print("❌ PAYHIP_API_KEY not set")
        return None

    print("🔐 PAYHIP KEY PREFIX:", PAYHIP_API_KEY[:5])

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}",
    }

    data = {
        "title": title,
        "description": description,
        "price": price,
        "currency": "INR",
    }

    print("🟣 Creating Payhip product with file upload...")

    with open(file_path, "rb") as f:
        files = {
            "file": f
        }

        r = requests.post(
            BASE_URL,
            headers=headers,
            data=data,
            files=files,
            timeout=60,
        )

    print("🟣 STATUS:", r.status_code)
    print("🟣 RESPONSE:", r.text[:500])

    if r.status_code not in [200, 201]:
        print("❌ Payhip publish failed")
        return None

    try:
        resp = r.json()
    except Exception:
        print("❌ Payhip did not return JSON")
        return None

    url = resp.get("permalink") or resp.get("url")

    print("🎉 PAYHIP PUBLISHED:", url)

    return url

