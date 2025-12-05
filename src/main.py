# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER
# Mission 2040 Engine — Batch 1 to Batch 9 Integrated
# -----------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings

# Core routers
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router

# Realtime dashboard API
from src.api_routes import router as realtime_api_router

# Intelligence API (Batch 6)
from src.router_intelligence import router as intelligence_router

# Batch 9 – Factory Engine Router
from src.router_factory import router as factory_router


# ------------------------------------------------------
# 1️⃣ Create FastAPI App
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 Engine",
)


# ------------------------------------------------------
# 2️⃣ Block legacy worker IP (safety)
# ------------------------------------------------------
BLOCKED_IP = "74.220.48.249"

@app.middleware("http")
async def block_old_ip(request: Request, call_next):
    client_ip = request.client.host
    if client_ip == BLOCKED_IP:
        return JSONResponse({"error": "Forbidden"}, status_code=403)
    return await call_next(request)


# ------------------------------------------------------
# 3️⃣ Register All Routers
# ------------------------------------------------------
app.include_router(health_router,   prefix="/api")
app.include_router(auth_router,     prefix="/api")
app.include_router(streams_router,  prefix="/api")
app.include_router(realtime_api_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(factory_router,  prefix="/api")  # ⭐ NEW Batch 9 Factory


# ------------------------------------------------------
# 4️⃣ Root Endpoint
# ------------------------------------------------------
@app.get("/")
def root():
    return {"message": "JRAVIS Backend API Active"}


# ------------------------------------------------------
# 5️⃣ Render Health Check Endpoint
# ------------------------------------------------------
@app.get("/healthz")
def render_health():
    return {"status": "ok"}
