from fastapi import APIRouter
from src.pricing.engine import generate_global_price

router = APIRouter(prefix="/pricing", tags=["Pricing AI"])


@router.post("/calc")
def calculate_price(stream: dict):
    """
    Input:
    {
        "name": "template-2001",
        "complexity": 1.3,
        "trending": 1.1
    }
    """
    result = generate_global_price(stream)
    return {
        "status": "ok",
        "stream": stream["name"],
        "pricing": result
    }
