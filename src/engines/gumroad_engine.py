import logging
from openai import OpenAI

logger = logging.getLogger("GumroadEngine")
client = OpenAI()


def _ask_openai(user_prompt: str, system_prompt: str | None = None) -> str:
    """
    Small internal helper so all calls are consistent and safe.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    return resp.choices[0].message.content


def run_gumroad_engine():
    """
    JRAVIS Phase-1: Create 1–2 high-quality digital products 
    for Gumroad (templates, planners, checklists, etc.).
    """
    logger.info("🟦 Running Gumroad Template Engine...")

    system_prompt = (
        "You are JRAVIS, an AI product creator for Gumroad. "
        "You must only generate legal, ethical, original content. "
        "Focus on high-demand digital templates (planners, trackers, business tools). "
        "No plagiarism. No copyrighted brands. No risky topics."
    )

    user_prompt = """
    Create a **single** high-value Gumroad digital product.

    Output in valid JSON with keys:
    - title: short, catchy product title
    - description: 2–3 paragraph sales copy
    - features: bullet list (5–8 bullet points)
    - target_audience: 1–2 sentence description
    - file_structure: what pages/sections the template will contain
    - suggested_price: price in USD (as a number)

    The product must be unique, useful, and sellable.
    """

    try:
        content = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Gumroad product spec generated.")
        logger.debug(f"Gumroad Product JSON:\n{content}")

        # 🔹 HOOK POINT:
        # Here you can call a publisher like:
        # from publishers.gumroad_publisher import publish_gumroad_product
        # publish_gumroad_product(content)

    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")
        raise
