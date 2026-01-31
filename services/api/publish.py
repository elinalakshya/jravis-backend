from fastapi import APIRouter, Header, HTTPException
import json
import os

from jravis_backend.services.security import check_lock_code
from jravis_backend.services.printify_service import (
    upload_image,
    create_product_draft,
)

router = APIRouter(prefix="/api/publish", tags=["POD"])


@router.post("/draft_pod/{pod_id}")
def draft_pod(
    pod_id: str,
    x_lock_code: str | None = Header(default=None, alias="X-LOCK-CODE"),
):
    # 🔐 Security
    check_lock_code(x_lock_code)

    # 📄 Load POD JSON
    pod_path = f"data/listings_pod/{pod_id}.json"
    if not os.path.exists(pod_path):
        raise HTTPException(status_code=404, detail="POD JSON not found")

    with open(pod_path, "r") as f:
        p = json.load(f)

    # 🖼 Upload image to Printify
    image_id = upload_image(p["design_image"])

    # 🧱 Correct Printify payload (ANGLE FIXED)
    payload = {
        "title": p["title"],
        "description": p["description"],
        "blueprint_id": p["blueprint_id"],
        "print_provider_id": p["print_provider_id"],
        "variants": p["variants"],
        "print_areas": [
            {
                "variant_ids": [v["id"] for v in p["variants"]],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1,
                                "angle": 0  # ✅ REQUIRED
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # 🏪 Create Printify draft product
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    if not shop_id:
        raise HTTPException(
            status_code=500,
            detail="PRINTIFY_SHOP_ID not set",
        )

    result = create_product_draft(shop_id, payload)

    return {
        "status": "success",
        "product_id": result["id"],
        "title": result["title"],
    }

