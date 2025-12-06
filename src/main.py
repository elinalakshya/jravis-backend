# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER
# Mission 2040 Engine — Batches 1 to 10 Active
# -----------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings

# Core routers
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router
from src.api_routes import router as realtime_api_router
from src.router_intelligence import router as intelligence_router
from src.router_factory import router as factory_router

# NEW Batch-10 uploader
from src.router_uploader import router as uploader_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend — Mission 2040 Engine",
)

BLOCKED_IP = "74.220.48.249"

@app.middleware("http")
async def block_old_ip(request: Request, call_next):
    if request.client.host == BLOCKED_IP:
        return JSONResponse({"error": "Forbidden"}, status_code=403)
    return await call_next(request)

# Register routers
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(streams_router, prefix="/api")
app.include_router(realtime_api_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(factory_router, prefix="/api")
app.include_router(uploader_router, prefix="/api")   # ⭐ NEW Batch-10

@app.get("/")
def root():
    return {"message": "JRAVIS Backend Active", "version": settings.VERSION}

@app.get("/healthz")
def health():
    return {"status": "ok"}
