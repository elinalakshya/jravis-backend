# src/intelligence/insights.py

from src.intelligence.revenue_tracker import get_today_revenue, get_week_revenue

def generate_insights():
    """Daily insight from real earnings."""
    today = get_today_revenue()

    if not today:
        return {"insight": "No revenue today yet. Keep scaling content and funnels."}

    top_stream = max(today, key=today.get)
    max_value = today[top_stream]

    return {
        "top_stream": top_stream,
        "earned": max_value,
        "insight": f"{top_stream} is performing strongest today. Increase focus on templates, funnels, traffic and scaling content."
    }


def generate_weekly_summary():
    weekly = get_week_revenue()

    if not weekly:
        return {"summary": "No revenue recorded this week yet."}

    highest = max(weekly, key=weekly.get)

    return {
        "weekly_revenue": weekly,
        "best_stream": highest,
        "best_value": weekly[highest],
        "summary": f"{highest} is leading this week. Double down next week."
    }
