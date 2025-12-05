# -----------------------------------------------------------
# JRAVIS Factory Engine — Batch 9
# Auto-Scaling Templates & Funnels Production System
# -----------------------------------------------------------

import random
import hashlib
import time


# -----------------------------------------------------------
# INTERNAL GENERATORS
# -----------------------------------------------------------
def generate_template():
    topics = ["business", "fitness", "finance", "lifestyle", "marketing", "ai tools"]
    niche = random.choice(topics)

    stamp = hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]

    return {
        "type": "template",
        "niche": niche,
        "file": f"template_{niche}_{stamp}.zip"
    }


def generate_funnel():
    goals = ["lead-gen", "affiliate", "newsletter", "course", "saas"]
    goal = random.choice(goals)

    stamp = hashlib.sha256(str(random.random()).encode()).hexdigest()[:10]

    return {
        "type": "funnel",
        "goal": goal,
        "file": f"funnel_{goal}_{stamp}.html"
    }


# -----------------------------------------------------------
# MASTER FACTORY BATCH
# -----------------------------------------------------------
def generate_factory_batch():
    batch = []

    # 1 Template
    batch.append(generate_template())

    # 1 Funnel
    batch.append(generate_funnel())

    # 1 “extra booster” asset
    batch.append({
        "type": "asset_pack",
        "file": f"assets_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}.zip"
    })

    return batch
