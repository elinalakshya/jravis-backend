# -----------------------------------------------------------
# Batch 12 — JRAVIS Growth Optimizer AI
# -----------------------------------------------------------

from fastapi import APIRouter
import time

router = APIRouter(prefix="/api/growth", tags=["Growth Optimizer"])


def compute_growth_score(perf):
    return (
        perf["clicks"] * 0.3 +
        perf["sales"] * 0.5 +
        perf["trend"] * 0.2
    )


@router.post("/evaluate")
async def evaluate_template(performance: dict):
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
    year = time.gmtime().tm_year

    base_year = 2026
    base_value = 4  # 4 Cr

    if year < base_year:
        return {"year": year, "target_cr": base_value}

    increment = (year - base_year) * 2  # +2 Cr per year
    target = base_value + increment

    return {"year": year, "target_cr": target}
