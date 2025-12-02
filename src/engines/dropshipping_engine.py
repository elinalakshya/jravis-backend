import logging
from openai import OpenAI
from publishers.dropshipping_publisher import save_dropshipping_product

logger = logging.getLogger("DropshippingEngine")
client = OpenAI()

def generate_dropshipping_product():
    """
    Creates:
    - Product title
    - Long description
    - Benefits
    - Marketing angle
    - Tags
    """
    prompt = """
    Create a dropshipping product listing.
    Include:
    - Title
    - Long description
    - Key benefits
    - Marketing angle
    - Tags list

    Return all as a single formatted text block.
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return r.choices[0].message["content"]


def run_dropshipping_engine():
    logger.info("🚚 Dropshipping Engine Running...")

    try:
        content = generate_dropshipping_product()

        title = "Dropshipping_Product"
        if "\n" in content:
            title = content.split("\n")[0].strip()

        save_dropshipping_product(title, content)

        logger.info("✅ Dropshipping Product Generated")

    except Exception as e:
        logger.error(f"❌ Dropshipping Engine Error: {e}")
