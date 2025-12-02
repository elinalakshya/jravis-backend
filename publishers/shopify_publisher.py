# publishers/shopify_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_shopify_product(task):
    """
    Creates product description + mock product content for Shopify.
    Manual upload needed (no API used).
    """
    print("🛒 Generating Shopify product listing...")

    try:
        prompt = """
        Write a Shopify digital product listing:
        - Title
        - Long description
        - Highlights
        - What’s included
        - How to use
        - Refund policy
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        desc = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/shopify_product.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(desc)

        print("🛍 Shopify product generated.")
        return "Shopify product generated"

    except Exception as e:
        print("❌ Shopify Error:", e)
        return "Shopify generation failed"
