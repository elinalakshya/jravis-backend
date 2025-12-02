import os
import logging
import requests

logger = logging.getLogger("SaaSPublisher")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_BASE = "https://api.stripe.com/v1"


def create_stripe_product(name, description):
    """Create a product in Stripe."""
    url = f"{STRIPE_BASE}/products"
    data = {
        "name": name,
        "description": description
    }

    try:
        r = requests.post(url, data=data, auth=(STRIPE_SECRET_KEY, ""), timeout=10)
        logger.info(f"[Stripe Product] {r.status_code} {r.text}")
        return r.json()
    except Exception as e:
        logger.error(f"❌ Error creating Stripe product: {e}")
        return None


def create_stripe_price(product_id, amount_in_rupees):
    """Create recurring monthly price."""
    url = f"{STRIPE_BASE}/prices"
    data = {
        "unit_amount": int(amount_in_rupees * 100),
        "currency": "inr",
        "recurring[interval]": "month",
        "product": product_id
    }

    try:
        r = requests.post(url, data=data, auth=(STRIPE_SECRET_KEY, ""), timeout=10)
        logger.info(f"[Stripe Price] {r.status_code} {r.text}")
        return r.json()
    except Exception as e:
        logger.error(f"❌ Error creating Stripe price: {e}")
        return None


def create_checkout_link(price_id):
    """Create payment link for the SaaS subscription."""
    url = f"{STRIPE_BASE}/payment_links"
    data = {
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1
    }

    try:
        r = requests.post(url, data=data, auth=(STRIPE_SECRET_KEY, ""), timeout=10)
        logger.info(f"[Stripe Payment Link] {r.status_code} {r.text}")
        return r.json().get("url")
    except Exception as e:
        logger.error(f"❌ Error generating Stripe checkout link: {e}")
        return None
