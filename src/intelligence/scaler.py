# src/intelligence/scaler.py

from src.intelligence.optimizer import SMART_SCALING_FACTORS

def get_scaling_factor(stream: str) -> float:
    """Return scaling factor for given stream."""
    return SMART_SCALING_FACTORS.get(stream, 1.0)
