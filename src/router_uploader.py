# -----------------------------------------------------------
# JRAVIS Batch-10 — Auto Marketplace Uploader API
# -----------------------------------------------------------

from fastapi import APIRouter
from src.marketplaces.simulated_client import upload_to_all

router = APIRouter(prefix="/api/uploader", tags=["Batch-10 Uploader"])

@router.post("/upload")
def upload_template(payload: dict):
    """
    Uploads a template to ALL marketplaces.
    Input:
        { "name": "template-2078.zip" }
    """
    template = payload.get("name")
    if not template:
        return {"error": "Template name missing"}

    return upload_to_all(template)
