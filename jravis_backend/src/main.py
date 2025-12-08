from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from jravis-backend.src.settings import settings

# Routers
from router_health import router as health_router
from router_factory import router as factory_router
from router_growth import router as growth_router
from router_files import router as files_router
from router_streams import router as streams_router
from router_revenue import router as revenue_router
from router_pricing import router as pricing_router
from router_uploader import router as uploader_router
from router_viral import router as viral_router
from router_intelligence import router as intelligence_router

app = FastAPI(title=settings.PROJECT_NAME)

# --------------------------- CORS ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- API KEY MIDDLEWARE --------------------
@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    path = request.url.path

    PUBLIC = ["/", "/healthz", "/api/health", "/files"]

    # Allow public endpoints
    if any(path.startswith(p) for p in PUBLIC):
        return await call_next(request)

    # Validate API key for protected routes
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        return JSONResponse({"error": "Missing API key"}, status_code=401)

    if api_key != settings.WORKER_KEY:
        return JSONResponse({"error": "Invalid API key"}, status_code=403)

    return await call_next(request)

# --------------------------- ROUTES -------------------------
app.include_router(health_router, prefix="/api")
app.include_router(factory_router, prefix="/api/factory")
app.include_router(growth_router, prefix="/api/growth")
app.include_router(files_router, prefix="/files")
app.include_router(streams_router, prefix="/api/streams")
app.include_router(revenue_router, prefix="/api/revenue")
app.include_router(pricing_router, prefix="/api/pricing")
app.include_router(uploader_router, prefix="/api/upload")
app.include_router(viral_router, prefix="/api/viral")
app.include_router(intelligence_router, prefix="/api/intelligence")

@app.get("/")
def root():
    return {"status": "JRAVIS Backend Online"}

@app.get("/healthz")
def health():
    return {"status": "ok"}
