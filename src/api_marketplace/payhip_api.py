# src/api_marketplace/payhip_api.py

from .api_manager import Keys

def payhip_revenue():
    if not Keys.payhip:
        return {"status": "no_key", "platform": "payhip"}

    # Payhip has no public API (as of 2025)
    # JRAVIS will only report that the key exists
    return {
        "platform": "payhip",
        "status": "key_available",
        "message": "Payhip API does not expose earnings. Manual dashboard sync only.",
    }
