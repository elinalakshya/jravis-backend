import os
import json
import requests
import logging
from db import get_db

GUMROAD_API = "https://api.gumroad.com/v2/products"


def publish_product_to_gumroad(product_id: str):
    token = os.getenv("GUMROAD_ACCESS_TOKEN")

    if not token:
        raise Exception("❌ Gumroad access token missing in env")

    conn = get_db()
    cur = conn.cursor()

    # ✅ products table stores JSON in payload column
    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("❌ Product not found in DB")

    try:
        product = json.loads(row[0])
    except Exception:
        raise Exception("❌ Invalid product JSON in DB")

    title = product.get("title")
    price = product.get("price", 199)

    if not title:
        raise Exception("❌ Product title missing in payload")

    payload = {
        "name": title,
        "price": int(price),
        "published": False  # ✅ draft product
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    logging.info("🚀 Creating Gumroad draft product")

    r = requests.post(GUMROAD_API, data=payload, headers=headers)

    if r.status_code != 200:
        raise Exception(f"❌ Gumroad API error {r.status_code}: {r.text}")

    data = r.json()

    if not data.get("success"):
        raise Exception(f"❌ Gumroad rejected: {data}")

    product_url = data["product"]["short_url"]

    return {
        "status": "success",
        "message": "✅ Product created as DRAFT on Gumroad",
        "gumroad_url": product_url
    }

