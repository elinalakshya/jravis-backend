import json
from fastapi import APIRouter, HTTPException

from services.gumroad_service import create_product, upload_file
from services.etsy_service import create_draft_listing
from services.printify_service import create_product as create_printify_product
from services.webflow_service import create_draft_item

router = APIRouter()


def load_listing(product_id):
    path = f"data/listings/{product_id}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        raise HTTPException(status_code=404, detail="Listing JSON not found")


@router.post("/api/publish/draft_all/{product_id}")
def draft_all(product_id: str):

    listing = load_listing(product_id)

    # ---- GUMROAD ----
    gum_id = create_product(
        listing["gumroad"]["title"],
        listing["price_inr"],
        listing["gumroad"]["description"]
    )
    upload_file(gum_id, listing["file_path"])

    # ---- ETSY ----
    create_draft_listing(
        listing["etsy"]["title"],
        listing["etsy"]["description"],
        listing["etsy"]["tags"]
    )

    # ---- PRINTIFY ----
    create_printify_product(listing["printify"]["title"])

    # ---- WEBFLOW ----
    create_draft_item(
        listing["webflow"]["slug"],
        listing["title"],
        listing["webflow"]["body"]
    )

    return {"status": "draft_created_on_all_platforms"}
