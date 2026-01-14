import os
import json
import requests
import logging

from db import get_db

GUMROAD_API_BASE = "https://api.gumroad.com/v2"
GUMROAD_TOKEN = os.getenv("GUMROAD_API_KEY")  # must start with k...


def publish_product_to_gumroad(product_id: str):
    if not GUMROAD_TOKEN:
        raise Exception("GUMROAD_API_KEY not set in environment")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()

    if not row:
        raise Exception("Product not found in DB")

    try:
        product = json.loads(row[0])
    except Exception as e:
        raise Exception(f"Invalid product JSON in DB: {str(e)}")

    title = product.get("title", "Digital Product")
    description = product.get("description", "")
    price = int(product.get("price", 99))

    payload = {
        "name": title,
        "price": price,
        "description": description,
        "published": True,
    }

    headers = {
        "Authorization": f"Bearer {GUMROAD_TOKEN}",
    }

    logging.info("🚀 Sending product to Gumroad")

    resp = requests.post(
        f"{GUMROAD_API_BASE}/products",
        headers=headers,
        data=payload,
        timeout=30,
    )

    if resp.status_code != 200:
        raise Exception(
            f"Gumroad API error: {resp.status_code} {resp.text}"
        )

    data = resp.json()

    if not data.get("success"):
        raise Exception(f"Gumroad rejected: {data}")

    gumroad_product = data["product"]

    # Save Gumroad product id
    try:
        cur.execute(
            "ALTER TABLE products ADD COLUMN gumroad_id TEXT"
        )
    except:
        pass

    cur.execute(
        "UPDATE products SET gumroad_id = ? WHERE id = ?",
        (gumroad_product["id"], product_id),
    )

    conn.commit()
    conn.close()

    logging.info("✅ Published on Gumroad")

    return {
        "gumroad_product_id": gumroad_product["id"],
        "url": gumroad_product["short_url"],
    }

