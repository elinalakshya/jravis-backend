from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "JRAVIS Backend is running"}

# IMPORTANT: Render requires this EXACT endpoint
@router.get("/healthz")
def render_health_check():
    return {"status": "ok"}
