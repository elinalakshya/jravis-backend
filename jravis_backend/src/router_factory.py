from fastapi import APIRouter
import uuid, os, zipfile

router = APIRouter()

@router.post("/generate")
def generate_template():
    name = f"template-{uuid.uuid4().hex[:4]}"
    dir_path = "factory_output"
    os.makedirs(dir_path, exist_ok=True)

    zip_path = f"{dir_path}/{name}.zip"

    # Create REAL zip file
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("readme.txt", "JRAVIS template bundle")

    return {"status": "generated", "name": name, "zip": zip_path}

@router.post("/scale/{name}")
def scale(name: str):
    return {"status": "scaled", "name": name}

