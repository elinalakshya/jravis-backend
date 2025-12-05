# src/api_marketplace/api_manager.py

import os

class APIManager:
    """
    Safely retrieves API keys from environment variables.
    No keys are exposed. No placeholders are returned.
    """

    @staticmethod
    def get(key_name: str):
        value = os.getenv(key_name)
        if not value:
            return None
        return value


# PLATFORM-SPECIFIC KEY ACCESSORS
class Keys:
    gumroad = APIManager.get("GUMROAD_API_KEY")
    payhip = APIManager.get("PAYHIP_API_KEY")
    shopify_key = APIManager.get("SHOPIFY_API_KEY")
    shopify_secret = APIManager.get("SHOPIFY_API_SECRET")
    printify = APIManager.get("PRINTIFY_API_KEY")
    etsy = APIManager.get("ETSY_API_KEY")
    youtube = APIManager.get("YOUTUBE_API_KEY")
    stripe = APIManager.get("STRIPE_API_KEY")
    paypal = APIManager.get("PAYPAL_CLIENT_ID")
    paypal_secret = APIManager.get("PAYPAL_CLIENT_SECRET")
    kdp = APIManager.get("KDP_API_KEY")
    webflow = APIManager.get("WEBFLOW_API_KEY")
