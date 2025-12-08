from fastapi import APIRouter

router = APIRouter()

@router.get("")
@router.get("/")
def health_root():
    return {"status": "ok"}

@router.get("/healthz")
def health_ping():
    return {"status": "ok"}
