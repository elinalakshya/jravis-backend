import os
import requests
from typing import Dict
import re

# =====================================================
# Gumroad Configuration
# =====================================================

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_API_URL = "https://api.gumroad.com/v2/products"


# =====================================================
# Helpers
# =====================================================

def slugify(text: str) -> str:
    """
    Convert product title into URL-safe slug.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:50]


# =====================================================
# Publisher
# =====================================================

def publish_to_gumroad(product: Dict) -> Dict:
    """
    Publishes a product to Gumroad and returns the Gumroad product object.
    """

    if not GUMROAD_API_KEY:
        raise RuntimeError("❌ GUMROAD_API_KEY not configured in environment")

    slug = slugify(product["title"])

    # ✅ Payload (NO access_token here)
    payload = {
        "name": product["title"],
        "price": int(product["price"]) * 100,   # cents
        "description": product.get("description", ""),
        "url": slug,
        "published": True,
    }

    # ✅ Authorization via Bearer token (important)
    headers = {
        "Accept": "application/json",
        "User-Agent": "JRAVIS-BOT/1.0",
        "Authorization": f"Bearer {GUMROAD_API_KEY}",
    }

    # 🌐 Call Gumroad API
    response = requests.post(
        GUMROAD_API_URL,
        headers=headers,
        data=payload,
        timeout=30,
    )

    # 🔍 Debug logs (visible in Render logs)
    print("🌐 Gumroad status:", response.status_code)
    print("🌐 Gumroad headers:", dict(response.headers))
    print("🌐 Gumroad raw response:", response.text[:500])

    # Parse JSON safely
    try:
        data = response.json()
    except Exception:
        raise RuntimeError(
            f"Gumroad returned non-JSON response "
            f"(status={response.status_code}): {response.text[:300]}"
        )

    # Gumroad API error handling
    if not data.get("success"):
        raise RuntimeError(f"Gumroad API error: {data}")

    # Return created product object
    return data.get("product", {})

