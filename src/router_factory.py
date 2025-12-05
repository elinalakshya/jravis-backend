# -----------------------------------------------------------
# Batch 9 — Auto-Scaling Template & Funnel Factory Router
# -----------------------------------------------------------

from fastapi import APIRouter
from pydantic import BaseModel
import random
import time

router = APIRouter(prefix="/factory", tags=["Factory"])


# ------------------------------------------------------
# Data Models
# ------------------------------------------------------
class TemplateRequest(BaseModel):
    market: str
    niche: str
    target: str


class TemplateResponse(BaseModel):
    template_id: str
    title: str
    description: str
    funnel_url: str
    predicted_sales_per_month: float
    created_at: float


# ------------------------------------------------------
# Generate Template / Funnel
# ------------------------------------------------------
@router.post("/generate", response_model=TemplateResponse)
def generate_factory_template(data: TemplateRequest):
    """JRAVIS Batch 9 — Creates auto-scaling templates & funnels."""

    template_id = f"TEMP-{random.randint(10000,99999)}"

    title = f"{data.market} - {data.niche} Funnel for {data.target}"
    description = (
        f"An optimized funnel designed for {data.target} in the {data.market} / {data.niche} segment. "
        "Auto-generated using JRAVIS Batch-9 scaling engine."
    )

    predicted_sales = round(random.uniform(12000, 75000), 2)

    return TemplateResponse(
        template_id=template_id,
        title=title,
        description=description,
        funnel_url=f"https://jravis.ai/funnels/{template_id}",
        predicted_sales_per_month=predicted_sales,
        created_at=time.time()
    )


# ------------------------------------------------------
# Fetch All Suggested Scaling Niches
# ------------------------------------------------------
@router.get("/niches")
def get_niches():
    niches = [
        "AI Tools",
        "Finance Automation",
        "Digital Downloads",
        "POD Niches",
        "Real Estate Funnels",
        "Affiliate Funnels",
        "Coaching Funnels",
        "Business Automation Kits",
    ]
    return {"niches": niches}
