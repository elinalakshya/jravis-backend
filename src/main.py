# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER
# Mission 2040 Engine — Batches 1 to 9 Activated
# -----------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings

# Core routers
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router

# Realtime Dashboard
from src.api_routes import router as realtime_api_router

# Intelligence (Batch 6)
from src.router_intelligence import router as intelligence_router

# Factory System (Batch 9)
from src.router_factory import router as factory_router


# ------------------------------------------------------
# 1️⃣ FastAPI App Init
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 Engine",
)


# ------------------------------------------------------
# 2️⃣ Block Legacy Worker IP
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
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(streams_router, prefix="/api")
app.include_router(realtime_api_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(factory_router, prefix="/api")   # ⬅ Batch-9


# ------------------------------------------------------
# 4️⃣ N8N Sync Webhook (Batch 8)
# ------------------------------------------------------
@app.post("/n8n/sync")
async def n8n_sync_handler(request: Request):
    """
    JRAVIS will accept pushes from N8N on this endpoint.
    Secured with a secret.
    """
    body = await request.json()
    incoming_secret = body.get("secret")

    if incoming_secret != settings.N8N_WEBHOOK_SECRET:
        return JSONResponse({"error": "Invalid secret"}, status_code=401)

    return {"status": "ok", "received": body}


# ------------------------------------------------------
# 5️⃣ Root Endpoint
# ------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "JRAVIS Backend API Active",
        "version": settings.VERSION,
        "mission": "Mission 2040: Passive Global Automation"
    }


# ------------------------------------------------------
# 6️⃣ Render Health Check
# ------------------------------------------------------
@app.get("/healthz")
def render_health():
    return {"status": "ok"}
