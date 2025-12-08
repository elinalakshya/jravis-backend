from fastapi import APIRouter

router = APIRouter()

@router.get("")
@router.get("/")
@router.get("/healthz")
def health():
    return {"status": "ok"}
