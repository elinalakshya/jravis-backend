import json
import uuid
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)


# ======================================================
# 🔎 SAFE DATA ROOT DETECTION (NO HARD PATH ASSUMPTIONS)
# ======================================================

def find_data_root() -> Path:
    """
    Walk upward from this file until we find a folder named 'data'.
    This works reliably across local, Docker, Render, CI, etc.
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        candidate = parent / "data"
        if candidate.exists():
            logging.info(f"📁 Data root detected at: {candidate}")
            return candidate

    raise RuntimeError("❌ Could not locate data directory in project tree")


DATA_ROOT = find_data_root()
DRAFT_DIR = DATA_ROOT / "drafts" / "templates"
PRODUCT_DIR = DATA_ROOT / "products"

PRODUCT_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================
# 📂 LOAD DRAFT
# ======================================================

def load_draft(draft_id: str) -> dict:
    """
    Load a draft JSON file by ID.
    """
    path = DRAFT_DIR / f"{draft_id}.json"
    logging.info(f"📂 Loading draft from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Draft not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================
# 🏗️ PRODUCT BUILDER CORE
# ======================================================

def build_product_from_draft(draft_id: str) -> dict:
    """
    Convert a draft into a sellable product object.
    """
    logging.info(f"🚀 Building product from draft: {draft_id}")

    draft = load_draft(draft_id)

    product_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # -------------------------
    # Product normalization
    # -------------------------
    product = {
        "id": product_id,
        "source_draft_id": draft_id,
        "title": draft.get("title"),
        "subtitle": draft.get("subtitle"),
        "description": draft.get("description"),
        "features": draft.get("features", []),
        "target_customer": draft.get("target_customer"),
        "tags": draft.get("tags", []),
        "price_suggestion": draft.get("price_suggestion"),
        "stream": draft.get("stream", "template"),

        # Product system fields
        "sku": f"JRAVIS-{product_id[:8].upper()}",
        "currency": "USD",
        "status": "draft",
        "created_at": now,
        "updated_at": now,

        # Marketplace readiness flags
        "assets_ready": False,
        "listing_ready": False,
        "published": False,
    }

    # -------------------------
    # Save product file
    # -------------------------
    product_path = PRODUCT_DIR / f"{product_id}.json"
    with open(product_path, "w", encoding="utf-8") as f:
        json.dump(product, f, indent=2)

    logging.info(f"💾 Product Saved → {product_path}")
    logging.info(f"✅ Product Built | ID={product_id} | SKU={product['sku']}")

    return {
        "status": "success",
        "product_id": product_id,
        "sku": product["sku"],
        "path": str(product_path),
        "title": product["title"],
    }


# ======================================================
# 🧪 LOCAL TEST MODE
# ======================================================

if __name__ == "__main__":
    # Example manual test:
    test_draft_id = "PUT_DRAFT_ID_HERE"

    try:
        result = build_product_from_draft(test_draft_id)
        print("✅ Product build result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        logging.exception("❌ Product build failed")

