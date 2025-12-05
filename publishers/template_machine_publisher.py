# File: publishers/template_machine_publisher.py
import os
import json
import time
from typing import Dict, Any

OUTPUT_DIR = "/opt/render/project/src/output/template_machine"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def publish_template_machine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Template Machine publisher (simulated).
    Saves reusable templates, scripts, SOPs or blueprints.
    """
    ensure_output_dir()

    timestamp = int(time.time())
    filename = f"{OUTPUT_DIR}/template_machine_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return {
            "publisher": "template_machine",
            "success": True,
            "message": "Template machine output saved",
            "file": filename,
            "data": payload,
        }

    except Exception as e:
        return {
            "publisher": "template_machine",
            "success": False,
            "error": str(e)
        }
