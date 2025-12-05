# src/router_factory.py

from fastapi import APIRouter
from src.factory.week_scheduler import generate_week_batch
from src.factory.scaling_engine import scale_decision

router = APIRouter(prefix="/factory", tags=["Factory"])


@router.get("/generate")
def generate_assets():
    batch = generate_week_batch()
    for item in batch:
        item["scaling_action"] = scale_decision(item)
    return {"created": batch, "count": len(batch)}
