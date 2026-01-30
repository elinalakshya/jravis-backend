from fastapi import APIRouter, HTTPException, Header
import os
import json

from jravis_backend.services.printify_service import (
    upload_image,
    create_product_draft,
)
from jravis_backend.services.security import check_lock_code

router = APIRouter(prefix="/api/publish", tags=["POD"])


@router.post("/draft_pod/{pod_id}")
def draft_pod(
    pod_id: str,
    x_lock_code: str = Header(default=None, alias="X-LOCK-CODE"),
):
    # -------------------------------
    # SECURITY
    # -------------------------------
    check_lock_code(x_lock_code)

    # -------------------------------
    # LOAD POD JSON
    # -------------------------------
    json_path = f"data/listings_pod/{pod_id}.json"

    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="POD JSON not found")

    with open(json_path, "r") as f:
        pod = json.load(f)

    # -------------------------------
    # VALIDATE REQUIRED FIELDS
    # -------------------------------
    required = [
        "title",
        "description",
        "blueprint_id",
        "print_provider_id",
        "variants",
        "design_image",
    ]

    for field in required:
        if field not in pod:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}",
            )

    # -------------------------------
    # UPLOAD IMAGE TO PRINTIFY
    # -------------------------------
    image_path = pod["design_image"]

    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=400,
            detail=f"Design image not found: {image_path}",
        )

    image_id = upload_image(image_path)

    # -------------------------------
    # SHOP ID
    # -------------------------------
    shop_id = os.getenv("PRINTIFY_SHOP_ID")
    if not shop_id:
        raise HTTPException(
            status_code=500,
            detail="PRINTIFY_SHOP_ID env variable not set",
        )

    # -------------------------------
    # BUILD PRINTIFY PAYLOAD
    # -------------------------------
    payload = {
        "title": pod["title"],
        "description": pod["description"],
        "blueprint_id": pod["blueprint_id"],
        "print_provider_id": pod["print_provider_id"],
        "variants": pod["variants"],
        "print_areas": [
            {
                "variant_ids": [v["id"] for v in pod["variants"]],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1,
                            }
                        ],
                    }
                ],
            }
        ],
    }

    # -------------------------------
    # CREATE DRAFT PRODUCT
    # -------------------------------
    result = create_product_draft(shop_id, payload)

    return {
        "status": "success",
        "product_id": result.get("id"),
        "title": result.get("title"),
    }

