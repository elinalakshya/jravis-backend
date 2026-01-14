# src/src/app.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uuid
import json
import logging

from db import init_db, get_db
from product_factory import generate_product
from listing_engine import generate_listing_from_product
from image_engine import generate_image_for_product, generate_images_for_all_products

from gumroad_oauth import get_auth_url, exchange_code_for_token, save_tokens
from gumroad_publisher import publish_product_to_gumroad

# ---------------------------------------------------
# App Init
# ---------------------------------------------------

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="JRAVIS Backend API")

init_db()

# ---------------------------------------------------
# Health
# ---------------------------------------------------

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# ---------------------------------------------------
# Product Builder
# ---------------------------------------------------

@app.post("/api/products/build")
def build_product(draft_id: str):
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

    return {"status": "success", "product": product}


# ---------------------------------------------------
# Bulk Product Generator
# ---------------------------------------------------

@app.post("/api/products/bulk_generate")
def bulk_generate_products(count: int = 10):

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

    return {"status": "success", "count": len(created), "products": created}


# ---------------------------------------------------
# Listing Generator
# ---------------------------------------------------

@app.post("/api/listings/generate")
def generate_listing(product_id: str):
    try:
        listing = generate_listing_from_product(product_id)
        return {"status": "success", "listing": listing}
    except Exception as e:
        logging.exception("❌ Listing generation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# Image Engine
# ---------------------------------------------------

@app.post("/api/products/generate_image")
def generate_image(product_id: str):
    try:
        path = generate_image_for_product(product_id)
        return {"status": "success", "product_id": product_id, "image_path": path}
    except Exception as e:
        logging.exception("❌ Image generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products/generate_images_all")
def generate_images_all():
    try:
        result = generate_images_for_all_products()
        return {"status": "success", **result}
    except Exception as e:
        logging.exception("❌ Bulk image generation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# Gumroad OAuth
# ---------------------------------------------------

@app.get("/api/auth/gumroad/start")
def gumroad_auth_start():
    url = get_auth_url()
    return RedirectResponse(url)


@app.get("/api/auth/gumroad/callback")
def gumroad_auth_callback(code: str):
    token_data = exchange_code_for_token(code)
    save_tokens(token_data)
    return {"status": "success", "message": "Gumroad connected successfully"}


# ---------------------------------------------------
# Gumroad Publisher
# ---------------------------------------------------

@app.post("/api/publish/gumroad")
def publish_to_gumroad(product_id: str):
    try:
        result = publish_product_to_gumroad(product_id)
        return {"status": "success", "gumroad": result}
    except Exception as e:
        logging.exception("❌ Gumroad publish failed")
        raise HTTPException(status_code=500, detail=str(e))
