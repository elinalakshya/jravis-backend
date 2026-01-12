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
        "price": int(product["price"]) * 100,   # Gumroad uses cents/paise
        "description": product.get("description", ""),
        "published": True
    }

    response = requests.post(GUMROAD_API_URL, data=payload, timeout=30)
    data = response.json()

    if not data.get("success"):
        raise RuntimeError(f"Gumroad error: {data}")

    return data["product"]
