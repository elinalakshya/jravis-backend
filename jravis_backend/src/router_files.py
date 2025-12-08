from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/factory_output/{filename}")
def get_factory_file(filename: str):
    file_path = os.path.join("factory_output", filename)

    if not os.path.exists(file_path):
        return {"error": "File not found", "path": file_path}

    return FileResponse(file_path, media_type="application/zip")
