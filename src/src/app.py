from product_builder import build_product_from_draft
from fastapi import FastAPI, Query
import os
from listing_engine import generate_listing_from_product
from draft_engine import (
    generate_and_save_template_draft,
    generate_batch_templates
)

app = FastAPI(title="JRAVIS Backend", version="2.0")

# ---------------------------
# Health
# ---------------------------

@app.get("/")
def root():
    return {"status": "ok", "service": "jravis"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


# ---------------------------
# Draft APIs
# ---------------------------

@app.post("/api/drafts/templates/generate")
def generate_single():
    draft, path = generate_and_save_template_draft()
    return {
        "status": "success",
        "draft": draft,
        "path": path
    }


@app.post("/api/drafts/templates/batch")
def generate_batch(count: int = Query(5, ge=1, le=50)):
    items = generate_batch_templates(count)
    return {
        "status": "success",
        "generated": len(items),
        "items": items
    }

@app.post("/api/products/build")
def build_product(draft_id: str):
    try:
        metadata = build_product_from_draft(draft_id)
        return {
            "status": "success",
            "product": metadata
        }
    except Exception as e:
        import traceback
        print("🔥 PRODUCT BUILD ERROR 🔥")
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e)
        }


@app.post("/api/listings/generate")
def generate_listing(product_id: str):
    listing = generate_listing_from_product(product_id)
    return {
        "status": "success",
        "listing": listing
    }
