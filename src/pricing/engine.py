# -----------------------------------------------------------
# JRAVIS — Batch 11 Global Pricing AI
# Hybrid Smart-Premium Model
# -----------------------------------------------------------

import random
import math

# FX reference table (auto-expanding later using API)
FX = {
    "INR": 83,
    "USD": 1,
    "EUR": 0.93,
    "GBP": 0.80,
    "AUD": 1.55,
    "CAD": 1.36
}

# Premium multipliers
PREMIUM_WEIGHTS = {
    "basic": 1.0,
    "standard": 1.4,
    "premium": 2.2
}


def estimate_value(stream):
    """
    Base value estimation based on:
    - design complexity
    - marketplace demand
    - trending score
    """
    base = random.randint(8, 25)  # base USD

    complexity_factor = stream.get("complexity", 1.0)
    trend = stream.get("trending", random.uniform(0.8, 1.5))

    return round(base * complexity_factor * trend, 2)


def apply_hybrid_pricing(base_value, tier):
    """Hybrid Smart–Premium Pricing Strategy"""
    weight = PREMIUM_WEIGHTS.get(tier, 1.0)
    return round(base_value * weight, 2)


def convert_currency(usd_price):
    """Return a dict of all prices in global currencies."""
    out = {}
    for cur, fx in FX.items():
        out[cur] = round(usd_price * fx, 2)
    return out


def generate_global_price(stream):
    """
    Entry point for pricing AI.
    """

    # Step 1 — Estimate base USD value
    base_value = estimate_value(stream)

    # Step 2 — Select tier (Hybrid smart-premium)
    tier = random.choice(["basic", "standard", "premium"])

    # Step 3 — Apply tier multiplier
    usd_price = apply_hybrid_pricing(base_value, tier)

    # Step 4 — Convert globally
    global_prices = convert_currency(usd_price)

    return {
        "tier": tier,
        "usd_price": usd_price,
        "prices": global_prices
    }
