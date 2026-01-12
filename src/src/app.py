from fastapi import FastAPI, HTTPException
import uuid
import json
import logging

from db import init_db, get_db, safe_json
from product_factory import generate_product
from listing_engine import generate_listing_from_product
from image_engine import generate_image_for_product, generate_images_for_all_products
from gumroad_publisher import publish_to_gumroad

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
                (product_id, safe_json(product))
            )

            created.append({
                "product_id": product_id,
                "title": product.get("title"),
                "price": product.get("price"),
                "sku": product.get("sku"),
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
# Single Image Generator API
# ---------------------------------------------------

@app.post("/api/products/generate_image")
def generate_image(product_id: str):
    try:
        image_path = generate_image_for_product(product_id)

        return {
            "status": "success",
            "product_id": product_id,
            "image_path": image_path
        }

    except Exception as e:
        logging.exception("❌ Image generation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# Bulk Image Generator API
# ---------------------------------------------------

@app.post("/api/products/generate_images_all")
def generate_images_all():
    try:
        result = generate_images_for_all_products()
        return {
            "status": "success",
            **result
        }

    except Exception as e:
        logging.exception("❌ Bulk image generation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# Gumroad Publisher API
# ---------------------------------------------------

@app.post("/api/publish/gumroad")
def publish_gumroad(product_id: str):
    try:
        result = publish_to_gumroad(product_id)
        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        logging.exception("❌ Gumroad publish failed")
        raise HTTPException(status_code=500, detail=str(e))

