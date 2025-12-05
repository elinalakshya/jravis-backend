from fastapi import APIRouter
from src.factory.zip_factory import (
    generate_template_package,
    scale_template,
    list_assets
)

router = APIRouter(prefix="/factory", tags=["Factory"])


@router.post("/generate")
def generate():
    """Generate a brand-new template ZIP."""
    return generate_template_package()


@router.post("/scale")
def scale(data: dict):
    """Scale a template into multiple variants."""
    base = data.get("base")
    count = int(data.get("count", 3))
    return scale_template(base, count)


@router.get("/list")
def list_all():
    """List all generated ZIP templates."""
    return list_assets()
