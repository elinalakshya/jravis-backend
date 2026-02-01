<<<<<<< HEAD
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
=======
# services/api/publish.py

import os
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from jravis_backend.services.printify_service import create_product_draft


router = APIRouter()


# =========================================================
# Request Model
# =========================================================

class PODDraftRequest(BaseModel):
    title: str
    description: str
    price: int
    design_image: str   # Printify image ID (NOT url)


# =========================================================
# Helpers
# =========================================================

LOCK_CODE = os.getenv("JRAVIS_LOCK_CODE")
SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


def verify_lock(code: str):
    if not LOCK_CODE or code != LOCK_CODE:
        raise HTTPException(status_code=401, detail="Invalid lock code")


# =========================================================
# Routes
# =========================================================

@router.post("/api/publish/draft_pod/{pod_id}")
def draft_pod(
    pod_id: str,
    payload: PODDraftRequest,
    x_lock_code: str = Header(None)
):
    """
    Create Printify draft product

    Requires:
    - title
    - description
    - price
    - design_image (Printify image ID)

    Security:
    - X-LOCK-CODE header required
    """

    # 🔐 Lock protection
    verify_lock(x_lock_code)

    if not SHOP_ID:
        raise HTTPException(status_code=500, detail="PRINTIFY_SHOP_ID missing in env")

    try:
        product_payload = {
            "title": payload.title,
            "description": payload.description,
            "price": payload.price,
            "design_image": payload.design_image
        }

        result = create_product_draft(SHOP_ID, product_payload)

        return {
            "status": "success",
            "pod_id": pod_id,
            "product": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> ba32f27 (fix publish route)

