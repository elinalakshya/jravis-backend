import os
import json
import uuid
import logging
from datetime import datetime

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

# Render safe project root
PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/opt/render/project/src")

DRAFT_DIR = os.path.join(PROJECT_ROOT, "data", "drafts", "templates")
PRODUCT_DIR = os.path.join(PROJECT_ROOT, "data", "products")

os.makedirs(PRODUCT_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def load_draft(draft_id: str) -> dict:
    """
    Load draft JSON from disk safely.
    """
    path = os.path.join(DRAFT_DIR, f"{draft_id}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Draft not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_product(product: dict) -> str:
    """
    Save product metadata to disk.
    """
    product_id = product["id"]
    path = os.path.join(PRODUCT_DIR, f"{product_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(product, f, indent=2)

    logging.info(f"📦 Product Saved → {path}")
    return path


# ---------------------------------------------------------
# CORE ENGINE
# ---------------------------------------------------------

def build_product_from_draft(draft_id: str) -> dict:
    """
    Convert a Draft into a Product entity.
    """

    draft = load_draft(draft_id)

    product_id = str(uuid.uuid4())

    product = {
        "id": product_id,
        "source_draft_id": draft_id,
        "title": draft.get("title"),
        "subtitle": draft.get("subtitle"),
        "description": draft.get("description"),
        "features": draft.get("features", []),
        "tags": draft.get("tags", []),
        "target_customer": draft.get("target_customer"),
        "price_suggestion": draft.get("price_suggestion"),
        "category": infer_category(draft),
        "platform_targets": infer_platforms(draft),
        "assets_required": infer_assets(draft),
        "status": "ready_for_listing",
        "created_at": datetime.utcnow().isoformat()
    }

    save_product(product)

    logging.info(
        f"🚀 Product Built | ID={product_id} | Title={product['title']}"
    )

    return product


# ---------------------------------------------------------
# INTELLIGENCE LAYERS (simple rules now — upgrade later)
# ---------------------------------------------------------

def infer_category(draft: dict) -> str:
    title = (draft.get("title") or "").lower()

    if "notion" in title:
        return "Notion Templates"
    if "excel" in title:
        return "Excel Tools"
    if "planner" in title or "printable" in title:
        return "Printables"
    if "canva" in title:
        return "Canva Templates"

    return "Digital Products"


def infer_platforms(draft: dict) -> list:
    """
    Decide where this product should be listed.
    """
    platforms = ["gumroad", "payhip"]

    title = (draft.get("title") or "").lower()

    if "printable" in title or "planner" in title:
        platforms.append("etsy")

    if "notion" in title or "canva" in title:
        platforms.append("etsy")

    return list(set(platforms))


def infer_assets(draft: dict) -> list:
    """
    Decide what assets must be created later.
    """
    assets = ["cover_image", "product_description", "preview_images"]

    title = (draft.get("title") or "").lower()

    if "excel" in title:
        assets.append("xlsx_template")

    if "notion" in title:
        assets.append("notion_template")

    if "printable" in title:
        assets.append("pdf_printable")

    return assets

