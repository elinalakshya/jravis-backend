import os
import json
import requests
import logging
from db import get_db

GUMROAD_API = "https://api.gumroad.com/v2/products"


def get_gumroad_token():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT access_token FROM gumroad_tokens ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return row[0]


def publish_product_to_gumroad(product_id: str):
    token = get_gumroad_token()
    if not token:
        raise Exception("❌ Gumroad not connected. Please run OAuth first.")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise Exception("❌ Product not found in DB")

    try:
        product = json.loads(row[0])
    except Exception as e:
        raise Exception(f"❌ Invalid product JSON in DB: {e}")

    title = product.get("title", "JRAVIS Digital Product")
    description = product.get("description", "")
    price = int(product.get("price", 199))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "name": title,
        "price": price * 100,   # Gumroad uses cents
        "description": description,
        "published": True
    }

    r = requests.post(GUMROAD_API, headers=headers, data=data)

    try:
        resp = r.json()
    except Exception:
        raise Exception(f"Gumroad API error {r.status_code}: {r.text}")

    if not resp.get("success"):
        raise Exception(f"Gumroad API error: {resp}")

    return {
        "status": "success",
        "gumroad_product_id": resp["product"]["id"],
        "url": resp["product"]["short_url"]
    }

