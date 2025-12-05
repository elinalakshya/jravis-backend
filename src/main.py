# src/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router

# ------------------------------------------------------
# 1️⃣ Create FastAPI app FIRST (so @app.middleware works)
# ------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API"
)

# ------------------------------------------------------
# 2️⃣ Block old caller IP (74.220.48.249)
# ------------------------------------------------------
BLOCKED_IP = "74.220.48.249"

@app.middleware("http")
async def block_old_caller(request: Request, call_next):
    client_ip = request.client.host
    if client_ip == BLOCKED_IP:
        return JSONResponse({"error": "Forbidden"}, status_code=403)
    return await call_next(request)

# ------------------------------------------------------
# 3️⃣ Routers
# ------------------------------------------------------
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(streams_router, prefix="/api")

# ------------------------------------------------------
# 4️⃣ Root endpoint
# ------------------------------------------------------
@app.get("/")
def root():
    return {"message": "JRAVIS Backend API Active"}

# ------------------------------------------------------
# 5️⃣ Render healthcheck fallback
# ------------------------------------------------------
@app.get("/healthz")
def render_health_check_root():
    return {"status": "ok"}
