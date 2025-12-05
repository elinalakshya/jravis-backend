# src/factory/funnel_engine.py

import random
import hashlib
from datetime import datetime

FUNNEL_TYPES = [
    "Lead Magnet Funnel",
    "Affiliate Review Funnel",
    "AI Automation Funnel",
    "Digital Product Sales Funnel",
    "Newsletter Signup Funnel",
    "Course Pre-launch Funnel",
]

def generate_unique_seed():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()[:10]


def generate_funnel():
    ftype = random.choice(FUNNEL_TYPES)
    tag = generate_unique_seed()

    funnel = {
        "id": f"FUNNEL-{tag}",
        "type": ftype,
        "title": f"{ftype} — {tag}",
        "conversion_goal": random.choice(["Leads", "Sales", "Subscribers"]),
        "quality_score": random.randint(75, 96),
        "created_at": datetime.utcnow().isoformat(),
    }

    return funnel
