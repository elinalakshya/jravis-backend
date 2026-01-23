import os
import json
import requests
import logging
from db import get_db

GUMROAD_CREATE_URL = "https://api.gumroad.com/v2/products"


def publish_product_to_gumroad(product_id: str):
    token = os.getenv("GUMROAD_ACCESS_TOKEN")

    if not token:
        raise Exception("❌ Gumroad access token missing in env")

    conn = get_db()
    cur = conn.cursor()

    # products table uses id, not product_id column
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
        raise Exception("❌ Product title missing")

    # Gumroad expects price in CENTS
    price_cents = int(float(price) * 100)

    payload = {
        "name": title,
        "price": price_cents,
        "published": False  # DRAFT
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    logging.info("🚀 Creating Gumroad draft product")

    r = requests.post(GUMROAD_CREATE_URL, data=payload, headers=headers)

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

from fastapi import APIRouter
import os, requests

router = APIRouter()

@router.post("/gumroad/publish")
def publish_to_gumroad(product: dict):
    token = os.getenv("GUMROAD_TOKEN")

    # 1. Create product
    create_url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": token,
        "name": product["title"],
        "price": int(product["price"] * 100),
        "description": product["description"]
    }
    r = requests.post(create_url, data=data).json()

    if not r.get("success"):
        return {"error": "create_failed", "details": r}

    product_id = r["product"]["id"]

    # 2. Upload file
    upload_url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    with open(product["file_path"], "rb") as f:
        files = {"file": f}
        data = {"access_token": token}
        u = requests.post(upload_url, files=files, data=data).json()

    if not u.get("success"):
        return {"error": "upload_failed", "details": u}

    # 3. Publish product
    pub_url = f"https://api.gumroad.com/v2/products/{product_id}"
    p = requests.put(pub_url, data={
        "access_token": token,
        "published": True
    }).json()

    return {
        "status": "published",
        "product_id": product_id,
        "url": r["product"]["short_url"]
    }
