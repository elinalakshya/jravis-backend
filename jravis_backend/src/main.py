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

# Health
app.include_router(health_router, prefix="")

# Factory
app.include_router(factory_router, prefix="/api/factory")

# Growth
app.include_router(growth_router, prefix="/api/growth")

# Files
app.include_router(files_router, prefix="/files")

# Streams
app.include_router(streams_router, prefix="/api/streams")

# Revenue
app.include_router(revenue_router, prefix="/api/revenue")

# Pricing
app.include_router(pricing_router, prefix="/api/pricing")

# Uploader
app.include_router(uploader_router, prefix="/api/upload")

# Viral
app.include_router(viral_router, prefix="/api/viral")

# Intelligence
app.include_router(intelligence_router, prefix="/api/intelligence")

