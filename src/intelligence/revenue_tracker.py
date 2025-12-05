# src/intelligence/revenue_tracker.py

import datetime

# In-memory logs (replace with DB later)
DAILY_REVENUE = {}
WEEKLY_REVENUE = {}


def log_revenue(stream: str, amount: float):
    """Store REAL income only."""
    today = datetime.date.today().isoformat()

    if today not in DAILY_REVENUE:
        DAILY_REVENUE[today] = {}

    DAILY_REVENUE[today][stream] = amount

    return {"status": "logged", "stream": stream, "amount": amount}


def get_today_revenue():
    """Return only REAL earnings. Zero means zero — not simulated."""
    today = datetime.date.today().isoformat()
    return DAILY_REVENUE.get(today, {})


def get_week_revenue():
    """Aggregate the last 7 days of REAL earnings."""
    weekly = {}
    today = datetime.date.today()

    for i in range(7):
        d = (today - datetime.timedelta(days=i)).isoformat()
        if d in DAILY_REVENUE:
            for stream, amount in DAILY_REVENUE[d].items():
                weekly[stream] = weekly.get(stream, 0) + amount

    return weekly
