# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER
# Batch 6 Ready: Intelligence + Realtime + Streams
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


# ------------------------------------------------------
# 1️⃣ Create FastAPI App (must be first)
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 Engine",
)


# ------------------------------------------------------
# 2️⃣ Block legacy worker IP
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
# System Health + Auth
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Worker Streams API
app.include_router(streams_router, prefix="/api")

# Realtime Dashboard API
app.include_router(realtime_api_router, prefix="/api")

# Batch-6 Intelligence API
app.include_router(intelligence_router, prefix="/api")


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
