from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Settings
from jravis_backend.src.settings import settings

# Routers
from jravis_backend.src.router_health import router as health_router
from jravis_backend.src.router_factory import router as factory_router
from jravis_backend.src.router_growth import router as growth_router
from jravis_backend.src.router_files import router as files_router
from jravis_backend.src.router_streams import router as streams_router
from jravis_backend.src.router_revenue import router as revenue_router
from jravis_backend.src.router_pricing import router as pricing_router
from jravis_backend.src.router_uploader import router as uploader_router
from jravis_backend.src.router_viral import router as viral_router
from jravis_backend.src.router_intelligence import router as intelligence_router

# ------------------------------------------------------
# CREATE APP (must ALWAYS come before include_router)
# ------------------------------------------------------
app = FastAPI(title=settings.PROJECT_NAME)

# ----------------------- CORS -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- API KEY CHECK -------------------
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    return await call_next(request)

# --------------------- ROUTERS ------------------------
app.include_router(health_router, prefix="")

