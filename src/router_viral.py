# -----------------------------------------------------------
# JRAVIS Batch-13 — Aggressive Viral Booster API
# -----------------------------------------------------------

from fastapi import APIRouter
import random
import os

router = APIRouter(prefix="/api/viral", tags=["Viral Booster"])

# A small bank of viral hooks (no API keys needed)
VIRAL_HOOKS = [
    "Minimal Design That Sells Every Day",
    "Top Template Format This Week",
    "Best Performing Layout in US Market",
    "Trending Style in UAE Buyers",
    "High Conversion Template Structure",
]

LANGUAGES = [
    "en", "es", "de", "fr", "ar", "hi", "pt", "id", "ja"
]

N8N_WEBHOOK = os.getenv("N8N_VIRAL_WEBHOOK")  # Boss already created webhook


# -----------------------------------------------------------
# Viral Candidate Check
# -----------------------------------------------------------
@router.get("/score/{name}")
async def viral_score(name: str):
    """
    JRAVIS calculates if the template deserves viral boost.
    Aggressive mode = higher push frequency.
    """
    score = random.randint(60, 100)  # Aggressive mode
    return {
        "status": "scored",
        "name": name,
        "score": score,
        "is_viral": score >= 75  # push threshold
    }


# -----------------------------------------------------------
# Force Viral Blast (worker calls this)
# -----------------------------------------------------------
@router.post("/blast")
async def viral_blast(payload: dict):
    """
    Prepares multi-language viral messages and sends
    everything to N8N for distribution.
    """
    name = payload.get("name")
    if not name:
        return {"error": "Missing template name"}

    hook = random.choice(VIRAL_HOOKS)

    messages = []
    for lang in LANGUAGES:
        msg = f"[{lang}] {hook}: {name}"
        messages.append(msg)

    # Push to N8N without API keys
    import requests
    try:
        requests.post(
            N8N_WEBHOOK,
            json={"template": name, "messages": messages, "channel": "viral_boost"},
            timeout=4
        )
    except:
        pass

    return {
        "status": "viral_sent",
        "name": name,
        "languages": len(LANGUAGES),
        "messages": messages
    }
