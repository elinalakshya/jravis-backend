from fastapi import APIRouter
from src.api_marketplace.aggregator import full_revenue_sync

router = APIRouter(prefix="/revenue", tags=["Revenue"])

@router.get("/live")
def live_revenue():
    return full_revenue_sync()
