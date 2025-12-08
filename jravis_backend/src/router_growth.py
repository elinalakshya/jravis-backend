from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/evaluate")
async def evaluate_growth(request: Request):

    # Safely try to read JSON body
    try:
        body = await request.json()
    except:
        body = {}

    name = body.get("name", "unknown")

    # Dummy output for now
    return {
        "template": name,
        "score": 50,
        "winner": False,
        "action": "pause"
    }
