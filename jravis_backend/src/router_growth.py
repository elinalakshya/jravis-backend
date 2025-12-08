# jravis_backend/src/router_growth.py

from fastapi import APIRouter, Request

router = APIRouter(prefix="/growth", tags=["Growth"])

# Existing GET route (keep it)
@router.get("/evaluate/{name}")
def evaluate(name: str):
    return {"template": name, "score": 50, "winner": False, "action": "pause"}

# NEW REQUIRED ROUTE FOR JRAVIS FRONTEND
@router.post("/evaluate")
async def evaluate_growth(request: Request):
    body = await request.json()

    # Placeholder logic — JRAVIS will replace later
    return {
        "input": body,
        "score": 72,
        "winner": True,
        "action": "scale"
    }
