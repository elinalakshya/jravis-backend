import os
import json
import requests
import logging
from db import get_db

GUMROAD_API_BASE = "https://api.gumroad.com/v2"

logging.basicConfig(level=logging.INFO)


def get_gumroad_token():
    """
    Get Gumroad access token from ENV.
    Token usually starts with 'k...'
    """
    token = os.getenv("GUMROAD_ACCESS_TOKEN")
    if not token:
        raise Exception("❌ Gumroad not connected. Please run OAuth first.")
    return token


def publish_product_to_gumroad(product_id: str):
    """
    Publish a product stored in SQLite to Gumroad
    """

    # --------------------------------------------------
    # Fetch product from DB
    # --------------------------------------------------
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("❌ Product not found in DB")

    # payload is stored as JSON STRING
    try:
        product = json.loads(row["payload"])
    except Exception as e:
        raise Exception(f"❌ Invalid product JSON in DB: {e}")

    title = product.get("title")
    description = product.get("description", "")
    price = product.get("price", 199)

    if not title:
        raise Exception("❌ Product title missing")

    # Gumroad expects price in cents
    price_cents = int(price)

    # --------------------------------------------------
    # Send to Gumroad API
    # --------------------------------------------------
    token = get_gumroad_token()

    url = f"{GUMROAD_API_BASE}/products"

    data = {
        "name": title,
        "price": price_cents,
        "description": description,
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    logging.info("🚀 Publishing product to Gumroad...")
    res = requests.post(url, data=data, headers=headers)

    # --------------------------------------------------
    # Handle response
    # --------------------------------------------------
    try:
        result = res.json()
    except Exception:
        raise Exception(f"❌ Gumroad returned non-JSON response (status={res.status_code}): {res.text}")

    if not result.get("success"):
        raise Exception(f"❌ Gumroad API error: {result}")

    product_info = result.get("product", {})

    gumroad_id = product_info.get("id")
    short_url = product_info.get("short_url")

    logging.info(f"✅ Published to Gumroad: {short_url}")

    return {
        "gumroad_product_id": gumroad_id,
        "url": short_url,
        "title": title,
        "price": price
    }

