from fastapi import APIRouter, Request

router = APIRouter(tags=["Growth"])   # FIXED prefix

@router.get("/evaluate/{name}")
def evaluate(name: str):
    return {"template": name, "score": 50, "winner": False, "action": "pause"}

@router.post("/evaluate")
async def evaluate_growth(request: Request):
    body = await request.json()
    return {
        "input": body,
        "score": 72,
        "winner": True,
        "action": "scale"
    }
    
