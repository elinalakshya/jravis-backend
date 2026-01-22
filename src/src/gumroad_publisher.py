import os
import json
import requests
import logging
from db import get_db

GUMROAD_API = "https://api.gumroad.com/v2/products"

logger = logging.getLogger(__name__)


def get_access_token():
    # Prefer ENV token (simpler, stable)
    token = os.getenv("GUMROAD_ACCESS_TOKEN")
    if token:
        return token

    # Fallback: token from DB (OAuth flow)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT access_token FROM gumroad_tokens ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if row:
        return row[0]

    return None


def publish_product_to_gumroad(product_id: str):
    token = get_access_token()
    if not token:
        return {"detail": "❌ Gumroad not connected. Please run OAuth first."}

    # ---- Fetch product payload ----
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return {"detail": "❌ Product not found in DB"}

    try:
        product = json.loads(row[0])
    except Exception as e:
        return {"detail": f"❌ Invalid product JSON: {str(e)}"}

    title = product.get("title")
    price = product.get("price", 99)
    description = product.get("description", "")
    tags = ",".join(product.get("tags", []))

    if not title:
        return {"detail": "❌ Product title missing"}

    # Gumroad price is in cents
    price_cents = int(price) * 100

    payload = {
        "name": title,
        "price": price_cents,
        "description": description,
        "tags": tags,
        "published": False,  # DRAFT MODE
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        resp = requests.post(GUMROAD_API, data=payload, headers=headers, timeout=30)
    except Exception as e:
        logger.exception("Gumroad request failed")
        return {"detail": f"❌ Gumroad request failed: {str(e)}"}

    if resp.status_code != 200:
        return {
            "detail": f"❌ Gumroad API error {resp.status_code}: {resp.text}"
        }

    data = resp.json()

    if not data.get("success"):
        return {"detail": f"❌ Gumroad rejected: {data}"}

    product_url = data["product"]["short_url"]

    return {
        "status": "success",
        "message": "✅ Product created as DRAFT on Gumroad",
        "gumroad_url": product_url,
    }

