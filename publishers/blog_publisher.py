# File: publishers/blog_publisher.py
import os
import json
import time
from typing import Dict, Any

OUTPUT_DIR = "/opt/render/project/src/output/blog"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def publish_blog(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Blog publisher (simulated).
    Saves blog article JSON for Webflow or WordPress automation.
    """
    ensure_output_dir()

    timestamp = int(time.time())
    filename = f"{OUTPUT_DIR}/blog_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return {
            "publisher": "blog",
            "success": True,
            "message": "Blog publish simulated",
            "file": filename,
            "data": payload
        }

    except Exception as e:
        return {
            "publisher": "blog",
            "success": False,
            "error": str(e)
        }
