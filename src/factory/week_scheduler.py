# src/factory/week_scheduler.py

import random
from src.factory.template_engine import generate_template
from src.factory.funnel_engine import generate_funnel

def generate_week_batch():
    count = random.randint(5, 7)  # B1 MODE

    items = []
    for _ in range(count):
        if random.random() < 0.6:
            items.append(generate_template())
        else:
            items.append(generate_funnel())

    return items
