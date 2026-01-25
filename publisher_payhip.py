import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")

BASE_URL = "https://payhip.com/api/v2/products"


def publish_to_payhip(title, description, file_path, price=199):
    debug = {}

    if not PAYHIP_API_KEY:
        return {"error": "PAYHIP_API_KEY not set"}

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}",
    }

    data = {
        "title": title,
        "description": description,
        "price": price,
        "currency": "INR",
    }

    with open(file_path, "rb") as f:
        files = {"file": f}

        r = requests.post(
            BASE_URL,
            headers=headers,
            data=data,
            files=files,
            timeout=60,
        )

    debug["status_code"] = r.status_code
    debug["text"] = r.text[:1000]

    try:
        debug["json"] = r.json()
    except Exception:
        debug["json"] = None

    return debug

