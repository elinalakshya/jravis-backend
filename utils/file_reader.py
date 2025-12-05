# utils/file_reader.py
import os
import json

BASE_PATH = "/opt/render/project/src/output/"

def get_latest_file(stream_name: str):
    """Fetch the latest JSON output file from JRAVIS worker."""
    folder = os.path.join(BASE_PATH, stream_name)

    if not os.path.exists(folder):
        return None

    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    if not files:
        return None

    files.sort(reverse=True)  # latest timestamp first
    latest_path = os.path.join(folder, files[0])

    try:
        with open(latest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
