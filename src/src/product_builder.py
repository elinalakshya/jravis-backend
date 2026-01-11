import json
import uuid
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)


# ======================================================
# 📁 DATA ROOT RESOLUTION (SAFE FOR RENDER / DOCKER)
# ======================================================

def resolve_data_root() -> Path:
    """
    Resolve a writable data directory safely.
    Priority:
    1. If /opt/render/project/src/data exists → use it
    2. Else create ./data relative to project root
    3. Never crash the app
    """

    # Common Render path
    render_path = Path("/opt/render/project/src/data")

    if render_path.exists():
        logging.info(f"📁 Using Render data path: {render_path}")
        return render_path

    # Fallback → create local data directory
    local_path = Path(__file__).resolve().parents[2] / "data"
    local_path.mkdir(parents=True, exist_ok=True)

    logging.warning(f"⚠️ Render data path not found. Using local data path: {local_path}")
    return local_path


DATA_ROOT = resolve_data_root()

DRAFT_DIR = DATA_ROOT / "drafts" / "templates"
PRODUCT_DIR = DATA_ROOT / "products"

# Ensure directories always exist
DRAFT_DIR.mkdir(parents=True, exist_ok=True)
PRODUCT_DIR.mkdir(parents=True, exist_ok=True)

logging.info(f"📂 Draft dir  → {DRAFT_DIR}")
logging.info(f"📦 Product dir → {PRODUCT_DIR}")


# ======================================================
# 📂 LOAD DRAFT
# ======================================================

def load_draft(draft_id: str) -> dict:
    path = DRAFT_DIR / f"{draft_id}.json"
    logging.info(f"📂 Loading draft: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Draft not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================
# 🏗️ PRODUCT BUILDER
# ======================================================

def build_product_from_draft(draft_id: str) -> dict:
    logging.info(f"🚀 Building product from draft: {draft_id}")

    draft = load_draft(draft_id)

    product_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

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

        # System fields
        "sku": f"JRAVIS-{product_id[:8].upper()}",
        "currency": "USD",
        "status": "draft",
        "created_at": now,
        "updated_at": now,

        # Pipeline flags
        "assets_ready": False,
        "listing_ready": False,
        "published": False,
    }

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
# 🧪 LOCAL TEST
# ======================================================

if __name__ == "__main__":
    test_draft_id = "PUT_DRAFT_ID_HERE"

    try:
        result = build_product_from_draft(test_draft_id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        logging.exception("❌ Product build failed")
