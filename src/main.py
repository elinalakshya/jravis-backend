# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER (FIXED VERSION)
# -----------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings

# Core routers
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router

# Realtime Dashboard API
from src.api_routes import router as realtime_api_router

# Intelligence API (Batch 6)
from src.router_intelligence import router as intelligence_router

# Factory API (Batch 9)
from src.router_factory import router as factory_router

# Growth Optimizer (Batch 12)
from src.router_growth import router as growth_router


# ------------------------------------------------------
# FastAPI App Init
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 Engine",
)


# ------------------------------------------------------
# SECURITY: API KEY VALIDATION (for worker)
# ------------------------------------------------------
WORKER_KEY = settings.REPORT_API_CODE


@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    """
    BLOCK ONLY requests missing correct API-KEY
    (Fixes the 403 issue and removes IP blocking)
    """
    # Allow public endpoints
    open_paths = [
    "/",
    "/healthz",
    "/api/health",
    "/task/next",
    "/task/new"
]
    if request.url.path in open_paths:
        return await call_next(request)

    api_key = request.headers.get("X-API-KEY")

    # If no key → reject
    if not api_key:
        return JSONResponse({"error": "Missing API key"}, status_code=401)

    # If wrong key → reject
    if api_key != WORKER_KEY:
        return JSONResponse({"error": "Invalid API key"}, status_code=403)

    return await call_next(request)


# ------------------------------------------------------
# Register All Routers
# ------------------------------------------------------
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(streams_router, prefix="/api")
app.include_router(realtime_api_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(factory_router, prefix="/api")
app.include_router(growth_router, prefix="/api")  # Batch-12


# ------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "JRAVIS Backend API Active",
        "version": settings.VERSION,
        "mission": "Mission 2040: Passive Global Automation"
    }


# ------------------------------------------------------
# Render Health Check
# ------------------------------------------------------
@app.get("/healthz")
def render_health():
    return {"status": "ok"}
