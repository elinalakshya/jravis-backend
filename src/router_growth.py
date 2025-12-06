# -----------------------------------------------------------
# Batch 12 — JRAVIS Growth Optimizer AI (FIXED PREFIX)
# -----------------------------------------------------------

from fastapi import APIRouter
import time

# IMPORTANT: Main.py already adds /api prefix
# So here prefix must be ONLY "/growth"
router = APIRouter(prefix="/growth", tags=["Growth Optimizer"])


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

    increment = (year - base_year) * 2
    target = base_value + increment

    return {"year": year, "target_cr": target}
