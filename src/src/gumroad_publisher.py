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
    if not GUMROAD_API_KEY:
        raise RuntimeError("GUMROAD_API_KEY not configured")

    slug = slugify(product["title"])

    payload = {
        "name": product["title"],
        "price": int(product["price"]) * 100,   # cents
        "description": product.get("description", ""),
        "url": slug,
        "published": True,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "JRAVIS-BOT/1.0",
    }

    # ✅ Put access_token in query params (important)
    params = {
        "access_token": GUMROAD_API_KEY
    }

    response = requests.post(
        GUMROAD_API_URL,
        params=params,
        data=payload,
        headers=headers,
        timeout=30,
        allow_redirects=False,   # ✅ stop HTML redirect
    )

    print("🌐 Gumroad status:", response.status_code)
    print("🌐 Gumroad headers:", dict(response.headers))
    print("🌐 Gumroad raw response:", response.text[:500])

    # If Gumroad redirected, show it clearly
    if response.status_code in (301, 302, 303, 307, 308):
        raise RuntimeError(
            f"Gumroad redirected request (status={response.status_code}, "
            f"location={response.headers.get('Location')})"
        )

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

