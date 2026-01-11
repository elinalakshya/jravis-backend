import json
import uuid
import logging
from pathlib import Path
from datetime import datetime

# =========================
# GLOBAL DATA ROOT
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]   # /opt/render/project/src
DATA_ROOT = BASE_DIR / "data"
DRAFT_DIR = DATA_ROOT / "drafts" / "templates"
PRODUCT_DIR = DATA_ROOT / "products"

PRODUCT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)


# =========================
# LOAD DRAFT
# =========================

def load_draft(draft_id: str) -> dict:
    path = DRAFT_DIR / f"{draft_id}.json"

    logging.info(f"📂 Loading draft from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Draft not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# SAVE PRODUCT
# =========================

def save_product(product: dict) -> dict:
    product_id = product["id"]
    path = PRODUCT_DIR / f"{product_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(product, f, indent=2)

    logging.info(f"💾 Product Saved → {path}")
    return product


# =========================
# BUILD PRODUCT
# =========================

def build_product_from_draft(draft_id: str) -> dict:
    logging.info(f"🏗️ Building product from draft: {draft_id}")

    draft = load_draft(draft_id)

    product = {
        "id": str(uuid.uuid4()),
        "source_draft": draft_id,
        "title": draft.get("title"),
        "category": draft.get("category"),
        "audience": draft.get("audience"),
        "format": draft.get("format"),
        "price": round(draft.get("suggested_price", 9.99), 2),
        "features": draft.get("features", []),
        "created_at": datetime.utcnow().isoformat(),
        "status": "ready_for_listing"
    }

    save_product(product)

    logging.info(f"✅ Product Built | ID={product['id']} | Title={product['title']}")
    return product

