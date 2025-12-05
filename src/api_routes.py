# src/api_routes.py

import os
import json
from fastapi import APIRouter

router = APIRouter()

BASE_PATH = "/opt/render/project/src/output"

def read_latest_json(folder):
    folder_path = os.path.join(BASE_PATH, folder)
    if not os.path.exists(folder_path):
        return None

    files = sorted(
        [
            f for f in os.listdir(folder_path)
            if f.endswith(".json")
        ],
        reverse=True
    )

    if not files:
        return None

    file_path = os.path.join(folder_path, files[0])
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return None


# ------------------------------
# STREAM STATUS ENDPOINT
# ------------------------------
@router.get("/streams")
def get_stream_status():
    streams = []

    stream_names = [
        "gumroad",
        "payhip",
        "blog",
        "newsletter",
        "affiliate_funnel",
        "shopify",
        "template_machine"
    ]

    for name in stream_names:
        data = read_latest_json(name)
        streams.append({
            "name": name.capitalize(),
            "status": "OK" if data else "NOT RUN",
            "lastRun": data.get("timestamp", "—") if data else "—"
        })

    return streams


# ------------------------------
# EARNINGS ENDPOINT
# ------------------------------
@router.get("/earnings")
def get_earnings():
    earnings = 0

    stream_names = [
        "gumroad",
        "payhip",
        "blog",
        "newsletter",
        "affiliate_funnel",
        "shopify",
        "template_machine"
    ]

    for name in stream_names:
        data = read_latest_json(name)
        if data and "earnings" in data:
            earnings += data["earnings"]

    return {"total": earnings}


# ------------------------------
# LOG FEED ENDPOINT
# ------------------------------
@router.get("/logs")
def get_logs():
    log_path = "/opt/render/project/src/worker.log"

    if not os.path.exists(log_path):
        return []

    with open(log_path, "r") as f:
        lines = f.readlines()

    # Return last 50 logs
    return lines[-50:]
