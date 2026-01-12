import os
import requests
from typing import Dict

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_API_URL = "https://api.gumroad.com/v2/products"


def publish_to_gumroad(product: Dict) -> Dict:
    """
    Publishes product to Gumroad and returns Gumroad response.
    """

    if not GUMROAD_API_KEY:
        raise RuntimeError("GUMROAD_API_KEY not configured")

    payload = {
        "access_token": GUMROAD_API_KEY,
        "name": product["title"],
        "price": int(product["price"]) * 100,
        "description": product.get("description", ""),
        "published": True
    }

    response = requests.post(GUMROAD_API_URL, data=payload, timeout=30)

    # 🔍 DEBUG LOGGING
    print("🌐 Gumroad status:", response.status_code)
    print("🌐 Gumroad raw response:", response.text[:500])

    # If Gumroad did not return JSON, raise clear error
    try:
        data = response.json()
    except Exception:
        raise RuntimeError(
            f"Gumroad returned non-JSON response "
            f"(status={response.status_code}): {response.text[:200]}"
        )

    if not data.get("success"):
        raise RuntimeError(f"Gumroad API error: {data}")

    return data["product"]

