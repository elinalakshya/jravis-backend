
# -----------------------------------------------------------
# JRAVIS BACKEND — Mission 2040 Engine
# Batch 6 + Batch 7 + Batch 8 Integrated
# Includes:
#   ✔ Secure Auth (Password + PIN + Lock)
#   ✔ Intelligence Engine
#   ✔ Stream Worker API
#   ✔ Realtime Dashboard API
#   ✔ Global Revenue Marketplace API
# -----------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings

# Core Routers
from src.router_health import router as health_router
from src.router_auth import router as auth_router                    # legacy
from src.router_auth_secure import router as secure_auth_router     # Batch 7 secure auth
from src.router_streams import router as streams_router

# Realtime Dashboard API
from src.api_routes import router as realtime_api_router

# Intelligence API (Batch 6)
from src.router_intelligence import router as intelligence_router

# Revenue Aggregator API (Batch 8)
from src.router_revenue import router as revenue_router


# -----------------------------------------------------------
# 1️⃣ Create FastAPI App (must be FIRST)
# -----------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API — Mission 2040 AI Engine",
)


# -----------------------------------------------------------
# 2️⃣ Block Old Legacy Worker IP
# -----------------------------------------------------------
BLOCKED_IP = "74.220.48.249"

@app.middleware("http")
async def block_old_worker(request: Request, call_next):
    client_ip = request.client.host
    if client_ip == BLOCKED_IP:
        return JSONResponse({"error": "Forbidden"}, status_code=403)
    return await call_next(request)


# -----------------------------------------------------------
# 3️⃣ Register All Routers (Order Matters)
# -----------------------------------------------------------

# ✓ Health
app.include_router(health_router, prefix="/api")

# ✓ Auth (legacy compatibility + secure auth)
app.include_router(auth_router, prefix="/api")
app.include_router(secure_auth_router, prefix="/api")

# ✓ Worker Streams (Gumroad, Payhip, Shopify, Blog, etc.)
app.include_router(streams_router, prefix="/api")

# ✓ Realtime Dashboard API
app.include_router(realtime_api_router, prefix="/api")

# ✓ Intelligence Layer (Batch 6)
app.include_router(intelligence_router, prefix="/api")

# ✓ Revenue Marketplace API (Batch 8)
app.include_router(revenue_router, prefix="/api")


# -----------------------------------------------------------
# 4️⃣ Root Endpoint
# -----------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "JRAVIS Backend API Active",
        "version": settings.VERSION,
        "mission": "Mission 2040 — Fully Automated Legal Income Engine"
    }


# -----------------------------------------------------------
# 5️⃣ Render Health Check
# -----------------------------------------------------------
@app.get("/healthz")
def render_health():
    return {"status": "ok"}
