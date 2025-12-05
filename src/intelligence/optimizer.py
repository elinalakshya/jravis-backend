# src/intelligence/optimizer.py

from src.intelligence.revenue_tracker import get_today_revenue

SMART_SCALING_FACTORS = {}


def calculate_scaling():
    """
    Smart scaling compares REAL earnings today.
    If a stream earns more → scale up production.
    If earns zero → reduce load slightly.
    """

    today = get_today_revenue()
    scaling = {}

    for stream, income in today.items():
        if income > 0:
            scaling[stream] = 1.25  # +25% boost for winners
        else:
            scaling[stream] = 0.85  # -15% slowdown for non-earners

    global SMART_SCALING_FACTORS
    SMART_SCALING_FACTORS = scaling

    return scaling


def run_optimizer():
    """Main optimizer engine called daily/each cycle."""
    scaling = calculate_scaling()
    return {"success": True, "scaling": scaling}
