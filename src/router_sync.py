# -------------------------------------------------------
# JRAVIS Batch 8 — N8N Sync Router
# Sends real-time updates to n8n workflow
# -------------------------------------------------------

from fastapi import APIRouter
import requests
import os

router = APIRouter()

N8N_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_SECRET = os.getenv("N8N_WEBHOOK_SECRET")


@router.post("/sync/n8n")
def sync_to_n8n(payload: dict):
    if not N8N_URL:
        return {"error": "N8N webhook not configured"}

    headers = {
        "X-JRAVIS-SECRET": N8N_SECRET
    }

    try:
        res = requests.post(N8N_URL, json=payload, headers=headers, timeout=10)
        return {"status": "sent", "n8n_response": res.text}
    except Exception as e:
        return {"error": str(e)}
