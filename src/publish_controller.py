import os

def get_active_streams():
    streams = []

    if os.getenv("GUMROAD_API_KEY"):
        streams.append("gumroad")
    if os.getenv("PAYHIP_API_KEY"):
        streams.append("payhip")
    if os.getenv("PRINTIFY_API_KEY"):
        streams.append("printify")
    if os.getenv("SHOPIFY_API_KEY") and os.getenv("SHOPIFY_PASSWORD") and os.getenv("SHOPIFY_STORE_URL"):
        streams.append("shopify")

    # Always-running streams
    streams += [
        "auto_blogging",
        "newsletter",
        "affiliate_funnels",
        "template_machines",
        "dropshipping_content"
    ]

    return streams
