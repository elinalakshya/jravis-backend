# src/factory/scaling_engine.py

def scale_decision(asset):
    score = asset["quality_score"]

    if score >= 90:
        return "BOOST_HEAVY"
    if score >= 80:
        return "BOOST"
    if score >= 70:
        return "NORMAL"
    return "REBUILD"
