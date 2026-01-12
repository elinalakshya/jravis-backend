from gumroad_publisher import publish_to_gumroad
from image_engine import generate_product_image
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

# ---------------------------------------------------
# Product Image Generator API
# ---------------------------------------------------

@app.post("/api/products/generate_image")
def generate_image(product_id: str):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        product = json.loads(row["payload"])

        image_path = generate_product_image(product)
        product["image_path"] = image_path

        # Update DB with image path
        cur.execute(
            "UPDATE products SET payload = ? WHERE id = ?",
            (json.dumps(product), product_id)
        )

        conn.commit()
        conn.close()

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
    """
    Generate images for all products that do not yet have image_path.
    """

    generated = []
    skipped = []

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT id, payload FROM products")
        rows = cur.fetchall()

        for row in rows:
            product_id = row["id"]
            product = json.loads(row["payload"])

            # Skip if already has image
            if product.get("image_path"):
                skipped.append(product_id)
                continue

            image_path = generate_product_image(product)
            product["image_path"] = image_path

            cur.execute(
                "UPDATE products SET payload = ? WHERE id = ?",
                (json.dumps(product), product_id)
            )

            generated.append({
                "product_id": product_id,
                "image_path": image_path
            })

        conn.commit()
        conn.close()

    except Exception as e:
        logging.exception("❌ Bulk image generation failed")
        raise HTTPException(status_code=500, detail=str(e))

    logging.info(f"🖼️ Bulk images generated: {len(generated)}, skipped: {len(skipped)}")

    return {
        "status": "success",
        "generated": len(generated),
        "skipped": len(skipped),
        "images": generated
    }


# ---------------------------------------------------
# Gumroad Publisher API
# ---------------------------------------------------

@app.post("/api/publish/gumroad")
def publish_gumroad(product_id: str):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT payload FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        product = json.loads(row["payload"])

        gumroad_product = publish_to_gumroad(product)

        # Save gumroad info
        product["gumroad_id"] = gumroad_product.get("id")
        product["gumroad_url"] = gumroad_product.get("short_url")

        cur.execute(
            "UPDATE products SET payload = ? WHERE id = ?",
            (json.dumps(product), product_id)
        )

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "product_id": product_id,
            "gumroad_url": product["gumroad_url"]
        }

    except Exception as e:
        logging.exception("❌ Gumroad publish failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/publish/gumroad_all")
def publish_all_gumroad():
    """
    Publish all products that are not yet on Gumroad.
    """

    published = []
    skipped = []

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, payload FROM products")
        rows = cur.fetchall()

        for row in rows:
            product_id = row["id"]
            product = json.loads(row["payload"])

            if product.get("gumroad_id"):
                skipped.append(product_id)
                continue

            gumroad_product = publish_to_gumroad(product)
            product["gumroad_id"] = gumroad_product.get("id")
            product["gumroad_url"] = gumroad_product.get("short_url")

            cur.execute(
                "UPDATE products SET payload = ? WHERE id = ?",
                (json.dumps(product), product_id)
            )

            published.append({
                "product_id": product_id,
                "url": product["gumroad_url"]
            })

        conn.commit()
        conn.close()

    except Exception as e:
        logging.exception("❌ Bulk Gumroad publish failed")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "published": len(published),
        "skipped": len(skipped),
        "products": published
    }
