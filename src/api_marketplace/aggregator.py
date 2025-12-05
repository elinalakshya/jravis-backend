# src/api_marketplace/aggregator.py

from .gumroad_api import gumroad_revenue
from .payhip_api import payhip_revenue
from .shopify_api import shopify_revenue
from .printify_api import printify_revenue

def full_revenue_sync():
    return {
        "gumroad": gumroad_revenue(),
        "payhip": payhip_revenue(),
        "shopify": shopify_revenue("your-shop-name"),
        "printify": printify_revenue(),
    }
