import json
from typing import Dict, Any
from db import get_db


def find_product(product_id: str) -> Dict[str, Any]:
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"❌ Product not found in DB: {product_id}")

    return json.loads(row["payload"])


def generate_listing_from_product(product_id: str) -> Dict[str, Any]:
    product = find_product(product_id)

    listing = {
        "product_id": product["product_id"],
        "sku": product.get("sku"),
        "title": product.get("title"),
        "description": product.get("description"),
        "price": product.get("price"),
        "tags": product.get("tags", []),
        "status": "ready",
    }

    print("🚀 Listing generated from SQLite DB")
    return listing
