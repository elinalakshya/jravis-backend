from product_factory import generate_product
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import uuid
import json
import logging

from db import init_db, get_db
from listing_engine import generate_listing_from_product

# ---------------------------------------------------
# App Initialization
# ---------------------------------------------------

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="JRAVIS Backend API")

# Initialize SQLite DB on startup
init_db()


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# ---------------------------------------------------
# Product Builder API
# ---------------------------------------------------

@app.post("/api/products/build")
def build_product(draft_id: str):
    """
    Temporary simplified builder.
    Later this will read from drafts table.
    """

    # ⚠️ For now we mock product content until draft DB is wired
    product = {
        "title": "Study Digital Toolkit for Students",
        "description": "A printable productivity toolkit for focused learners.",
        "price": 199,
        "tags": ["study", "productivity", "planner", "printable"],
        "sku": f"JRAVIS-{uuid.uuid4().hex[:8].upper()}",
    }

    product_id = str(uuid.uuid4())
    product["product_id"] = product_id

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO products (id, payload) VALUES (?, ?)",
            (product_id, json.dumps(product))
        )

        conn.commit()
        conn.close()

    except Exception as e:
        logging.exception("❌ Failed to save product")
        raise HTTPException(status_code=500, detail=str(e))

    logging.info(f"✅ Product created in DB: {product_id}")

    return {
        "status": "success",
        "product": product
    }


# ---------------------------------------------------
# Listing Generator API
# ---------------------------------------------------

@app.post("/api/listings/generate")
def generate_listing(product_id: str):
    try:
        listing = generate_listing_from_product(product_id)
        return {
            "status": "success",
            "listing": listing
        }

    except Exception as e:
        logging.exception("❌ Listing generation failed")
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------
# Bulk Product Generator API
# ---------------------------------------------------

@app.post("/api/products/bulk_generate")
def bulk_generate_products(count: int = 10):
    """
    Generate multiple products and store into SQLite.
    """

    if count < 1 or count > 100:
        raise HTTPException(status_code=400, detail="count must be 1–100")

    created = []

    try:
        conn = get_db()
        cur = conn.cursor()

        for _ in range(count):
            product = generate_product()

            product_id = str(uuid.uuid4())
            product["product_id"] = product_id

            cur.execute(
                "INSERT INTO products (id, payload) VALUES (?, ?)",
                (product_id, json.dumps(product))
            )

            created.append({
                "product_id": product_id,
                "title": product["title"],
                "price": product["price"],
                "sku": product["sku"],
            })

        conn.commit()
        conn.close()

    except Exception as e:
        logging.exception("❌ Bulk generation failed")
        raise HTTPException(status_code=500, detail=str(e))

    logging.info(f"🚀 Bulk generated {len(created)} products")

    return {
        "status": "success",
        "count": len(created),
        "products": created
    }
