# -----------------------------------------------------------
# JRAVIS BACKEND — MASTER FASTAPI ROUTER (Batch 8 Ready)
# Mission 2040 Engine: Streams + Intelligence + N8N Sync
# -----------------------------------------------------------

from fastapi import FastAPI, Request, Header
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
# 1️⃣ Create FastAPI App
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 Engine",
)

# ------------------------------------------------------
# 2️⃣ Block legacy worker IP (old Render tests)
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

# ------------------------------------------------------
# 4️⃣ N8N Webhook Sync Router (NEW)
# ------------------------------------------------------
N8N_SECRET = settings.N8N_WEBHOOK_SECRET  # from Render environment

@app.post("/api/sync/n8n")
async def sync_from_n8n(
    request: Request,
    secret_header: str = Header(default=None, alias="X-JRAVIS-SECRET")
):
    """
    n8n → JRAVIS secure webhook entry point.
    """
    if secret_header != N8N_SECRET:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    payload = await request.json()
    print("📥 N8N → JRAVIS Sync Payload:", payload)

    return {"status": "ok", "received": payload}

# ------------------------------------------------------
# 5️⃣ Root Endpoint
# ------------------------------------------------------
@app.get("/")
def root():
    return {"message": "JRAVIS Backend API Active"}

# ------------------------------------------------------
# 6️⃣ Render Health Check
# ------------------------------------------------------
@app.get("/healthz")
def render_health():
    return {"status": "ok"}
