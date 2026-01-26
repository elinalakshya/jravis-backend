from product_factory import generate_product
from draft_store import save_draft
from datetime import datetime


def run_draft_engine(niche="general"):
    product = generate_product(niche)

    entry = {
        "title": product["title"],
        "niche": niche,
        "zip": product["zip_path"],
        "created_at": datetime.utcnow().isoformat()
    }

    save_draft(entry)
    return entry
