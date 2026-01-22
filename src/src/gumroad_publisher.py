import os
import requests
from db import get_db

GUMROAD_API = "https://api.gumroad.com/v2/products"
TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN")


def publish_product_to_gumroad(product_id: str):
    if not TOKEN:
        return {"error": "GUMROAD_ACCESS_TOKEN not set in env"}

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT title, price FROM products WHERE product_id = ?", (product_id,))
    row = cur.fetchone()

    if not row:
        return {"error": "Product not found in DB"}

    title, price = row

    data = {
        "name": title,
        "price": int(price) * 100,   # Gumroad uses cents
        "published": "false"         # keep as DRAFT
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        res = requests.post(GUMROAD_API, data=data, headers=headers, timeout=30)
    except Exception as e:
        return {"error": str(e)}

    if res.status_code != 200:
        return {
            "error": "Gumroad API failed",
            "status": res.status_code,
            "body": res.text
        }

    out = res.json()

    if not out.get("success"):
        return {"error": "Gumroad rejected request", "body": out}

    gumroad_id = out["product"]["id"]

    cur.execute(
        "UPDATE products SET gumroad_id = ? WHERE product_id = ?",
        (gumroad_id, product_id)
    )
    db.commit()

    return {
        "status": "draft_created",
        "gumroad_id": gumroad_id
    }
