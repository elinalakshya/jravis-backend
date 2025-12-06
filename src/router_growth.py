# -----------------------------------------------------------
# Batch 12 — JRAVIS Growth Optimizer AI
# -----------------------------------------------------------

from fastapi import APIRouter
import random
import time

router = APIRouter(prefix="/api/growth", tags=["Growth Optimizer"])


def compute_growth_score(perf):
    """Calculate performance quality score."""
    return (
        perf["clicks"] * 0.3 +
        perf["sales"] * 0.5 +
        perf["trend"] * 0.2
    )


@router.post("/evaluate")
async def evaluate_template(performance: dict):
    """
    Input example:
    {
        "name": "template-2099",
        "clicks": 120,
        "sales": 6,
        "trend": 1.4
    }
    """
    score = compute_growth_score(performance)
    is_winner = score > 40

    return {
        "template": performance["name"],
        "score": score,
        "winner": is_winner,
        "action": "scale" if is_winner else "pause"
    }


@router.get("/monthly-target")
async def monthly_target():
    """
    Returns the required growth goal for Mission 2040.
    """
    year = time.gmtime().tm_year

    base_year = 2026
    base_value = 4  # 4 Cr

    if year < base_year:
        return {"year": year, "target_cr": base_value}

    increment = (year - base_year) * 2  # +2 Cr per year
    target = base_value + increment

    return {"year": year, "target_cr": target}
