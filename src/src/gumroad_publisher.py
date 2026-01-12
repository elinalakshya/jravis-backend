import os
import requests
from typing import Dict
import re

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_API_URL = "https://api.gumroad.com/v2/products"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:50]


def publish_to_gumroad(product: Dict) -> Dict:
    """
    Publishes product to Gumroad and returns Gumroad product object.
    """

    if not GUMROAD_API_KEY:
        raise RuntimeError("GUMROAD_API_KEY not configured")

    slug = slugify(product["title"])

    payload = {
        "access_token": GUMROAD_API_KEY,
        "name": product["title"],
        "price": int(product["price"]) * 100,   # paise → cents
        "description": product.get("description", ""),
        "url": slug,                            # ✅ REQUIRED
        "published": True
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "JRAVIS-BOT/1.0"
    }

    response = requests.post(
        GUMROAD_API_URL,
        data=payload,
        headers=headers,
        timeout=30
    )

    print("🌐 Gumroad status:", response.status_code)
    print("🌐 Gumroad raw response:", response.text[:500])

    try:
        data = response.json()
    except Exception:
        raise RuntimeError(
            f"Gumroad returned non-JSON response "
            f"(status={response.status_code}): {response.text[:300]}"
        )

    if not data.get("success"):
        raise RuntimeError(f"Gumroad API error: {data}")

    return data["product"]

