# src/intelligence/market_pulse.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_market_pulse():
    """
    AI searches global patterns for demand spikes.
    No earnings involved — pure intelligence.
    """

    prompt = """
    Identify 5 trending digital product niches for the next 30 days.
    Must be legal, ethical, global, and scalable.
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message["content"]
