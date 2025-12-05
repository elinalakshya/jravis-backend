# File: publishers/payhip_publisher.py
import os
import json
import time
from typing import Dict, Any

OUTPUT_DIR = "/opt/render/project/src/output/payhip"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def publish_payhip(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Payhip publisher (simulated).
    Saves product listing JSON for n8n automation.
    """
    ensure_output_dir()

    timestamp = int(time.time())
    filename = f"{OUTPUT_DIR}/payhip_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return {
            "publisher": "payhip",
            "success": True,
            "message": "Payhip publish simulated successfully",
            "file": filename,
            "data": payload
        }

    except Exception as e:
        return {
            "publisher": "payhip",
            "success": False,
            "error": str(e)
        }
