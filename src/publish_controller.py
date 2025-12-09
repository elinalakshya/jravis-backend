import os

ENABLE_GUMROAD = os.getenv("GUMROAD_API_KEY") is not None
ENABLE_PAYHIP = os.getenv("PAYHIP_API_KEY") is not None
ENABLE_PRINTIFY = os.getenv("PRINTIFY_API_KEY") is not None
ENABLE_SHOPIFY = (
    os.getenv("SHOPIFY_API_KEY") and 
    os.getenv("SHOPIFY_PASSWORD") and 
    os.getenv("SHOPIFY_STORE_URL")
)

def get_active_streams():
    streams = []
    if ENABLE_GUMROAD: streams.append("gumroad")
    if ENABLE_PAYHIP: streams.append("payhip")
    if ENABLE_PRINTIFY: streams.append("printify")
    if ENABLE_SHOPIFY: streams.append("shopify")
    
    # Always-on content systems
    streams += [
        "auto_blogging",
        "newsletter",
        "affiliate_funnels",
        "template_machines",
        "dropshipping_content"
    ]
    return streams
