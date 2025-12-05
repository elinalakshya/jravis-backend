# -----------------------------------------------------------
# JRAVIS — Batch 9 Factory Router
# Auto-Scaling Templates & Funnels Factory
# -----------------------------------------------------------

from fastapi import APIRouter
from src.factory.engine import generate_factory_batch

router = APIRouter(prefix="/factory", tags=["Factory Engine"])

# -----------------------------------------------------------
# Generate new templates / funnels batch
# -----------------------------------------------------------
@router.get("/generate")
def run_factory():
    """
    Creates the next batch of auto-generated templates, funnels,
    store assets, landing pages, and file packs.
    """
    output = generate_factory_batch()

    return {
        "status": "ok",
        "generated": output
    }
